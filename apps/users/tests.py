from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import CustomUser


class UserRegistrationTest(TestCase):
    def setUp(self):
        # setUp викликається перед кожним тестом
        # Створюємо чистий API клієнт
        self.client = APIClient()
        self.register_url = reverse('auth-register')

    def test_register_success(self):
        """Успішна реєстрація нового користувача"""
        data = {
            'username': 'testuser',
            'email': 'test@test.com',
            'password': 'TestPass123!',
            'password2': 'TestPass123!',
            'role': 'seller',
        }
        response = self.client.post(self.register_url, data)

        # Перевіряємо статус відповіді
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Перевіряємо що користувач створений в БД
        self.assertTrue(CustomUser.objects.filter(username='testuser').exists())

    def test_register_passwords_dont_match(self):
        """Реєстрація з різними паролями повинна провалитись"""
        data = {
            'username': 'testuser2',
            'email': 'test2@test.com',
            'password': 'TestPass123!',
            'password2': 'WrongPass123!',
            'role': 'seller',
        }
        response = self.client.post(self.register_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Перевіряємо що користувач НЕ створений
        self.assertFalse(CustomUser.objects.filter(username='testuser2').exists())

    def test_register_duplicate_username(self):
        """Реєстрація з існуючим username повинна провалитись"""
        # Спочатку створюємо користувача
        CustomUser.objects.create_user(
            username='existing',
            password='TestPass123!'
        )

        data = {
            'username': 'existing',
            'email': 'new@test.com',
            'password': 'TestPass123!',
            'password2': 'TestPass123!',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('auth-login')

        # Створюємо тестового користувача
        self.user = CustomUser.objects.create_user(
            username='seller1',
            password='TestPass123!',
            role='seller'
        )

    def test_login_success(self):
        """Успішний логін повертає access і refresh токени"""
        data = {
            'username': 'seller1',
            'password': 'TestPass123!'
        }
        response = self.client.post(self.login_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Перевіряємо що в відповіді є токени
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_wrong_password(self):
        """Логін з неправильним паролем повинен провалитись"""
        data = {
            'username': 'seller1',
            'password': 'WrongPassword!'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_nonexistent_user(self):
        """Логін неіснуючого користувача повинен провалитись"""
        data = {
            'username': 'nobody',
            'password': 'TestPass123!'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserRoleTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_default_role_is_buyer(self):
        """За замовчуванням роль — buyer"""
        user = CustomUser.objects.create_user(
            username='newuser',
            password='TestPass123!'
        )
        self.assertEqual(user.role, CustomUser.BUYER)

    def test_default_account_type_is_basic(self):
        """За замовчуванням тип акаунту — basic"""
        user = CustomUser.objects.create_user(
            username='newuser2',
            password='TestPass123!'
        )
        self.assertEqual(user.account_type, CustomUser.BASIC)

    def test_is_premium_property(self):
        """Властивість is_premium повертає True для premium акаунту"""
        user = CustomUser.objects.create_user(
            username='premiumuser',
            password='TestPass123!',
            account_type='premium'
        )
        self.assertTrue(user.is_premium)

    def test_is_seller_property(self):
        """Властивість is_seller повертає True для seller"""
        user = CustomUser.objects