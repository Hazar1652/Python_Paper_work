from django.test import TestCase
from unittest.mock import patch
from apps.users.models import CustomUser
from apps.cars.models import Car, Make, CarModel
from .services import check_text_for_profanity, moderate_car
from .models import ModerationLog


class ProfanityCheckTest(TestCase):
    def test_clean_text(self):
        result = check_text_for_profanity('Чудовий автомобіль в ідеальному стані')
        self.assertEqual(result, [])

    def test_text_with_forbidden_word(self):
        result = check_text_for_profanity('Це spam оголошення')
        self.assertIn('spam', result)

    def test_case_insensitive(self):
        result = check_text_for_profanity('Це SPAM оголошення')
        self.assertIn('spam', result)

    def test_multiple_forbidden_words(self):
        result = check_text_for_profanity('spam and fraud here')
        self.assertIn('spam', result)
        self.assertIn('fraud', result)


class ModerationServiceTest(TestCase):
    def setUp(self):
        self.seller = CustomUser.objects.create_user(
            username='seller1',
            password='TestPass123!',
            role='seller',
            email='seller@test.com'
        )
        self.make = Make.objects.create(name='Toyota')
        self.model = CarModel.objects.create(name='Camry', make=self.make)

    def _create_car(self, description, edit_count=0):
        return Car.objects.create(
            owner=self.seller,
            make=self.make,
            model=self.model,
            year=2022,
            price=20000,
            currency='USD',
            description=description,
            status='pending',
            edit_count=edit_count
        )

    def test_clean_listing_gets_approved(self):
        car = self._create_car('Чудовий автомобіль')
        result = moderate_car(car.id)
        self.assertEqual(result['status'], 'approved')
        car.refresh_from_db()
        self.assertEqual(car.status, 'active')

    def test_flagged_listing_gets_flagged_status(self):
        car = self._create_car('Це spam оголошення')
        result = moderate_car(car.id)
        self.assertEqual(result['status'], 'flagged')
        car.refresh_from_db()
        self.assertEqual(car.status, 'flagged')

    def test_flagged_listing_shows_remaining_edits(self):
        car = self._create_car('spam опис', edit_count=1)
        result = moderate_car(car.id)
        self.assertEqual(result['edits_remaining'], 2)

    @patch('apps.notifications.tasks.send_listing_flagged_notification.delay')
    def test_seller_notified_when_flagged(self, mock_notify):
        """
        Мок перевіряє що Celery задача була викликана
        але не відправляє реальний email
        """
        car = self._create_car('spam опис')
        moderate_car(car.id)

        # Перевіряємо що задача була викликана
        mock_notify.assert_called_once_with(
            seller_email='seller@test.com',
            car_id=car.id,
            edits_remaining=3
        )

    @patch('apps.notifications.tasks.send_moderation_notification.delay')
    def test_managers_notified_when_deactivated(self, mock_notify):
        """
        Мок перевіряє що менеджери отримали сповіщення
        при деактивації оголошення
        """
        # Створюємо менеджера
        manager = CustomUser.objects.create_user(
            username='manager1',
            password='TestPass123!',
            role='manager',
            email='manager@test.com'
        )

        car = self._create_car('spam опис', edit_count=3)
        moderate_car(car.id)

        # Перевіряємо що задача була викликана для менеджера
        mock_notify.assert_called_once_with(
            manager_email='manager@test.com',
            car_id=car.id,
            reason='Ліміт редагувань вичерпано'
        )

    def test_listing_deactivated_after_3_edits(self):
        car = self._create_car('spam опис', edit_count=3)
        result = moderate_car(car.id)
        self.assertEqual(result['status'], 'deactivated')
        car.refresh_from_db()
        self.assertEqual(car.status, 'inactive')

    def test_moderation_log_created(self):
        car = self._create_car('Чудовий автомобіль')
        moderate_car(car.id)
        logs = ModerationLog.objects.filter(car=car)
        self.assertEqual(logs.count(), 1)
        self.assertEqual(logs.first().status, ModerationLog.APPROVED)

    def test_nonexistent_car(self):
        result = moderate_car(99999)
        self.assertIn('error', result)