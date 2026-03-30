from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.users.models import CustomUser
from .models import Car, Make, CarModel


class CarListingTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Створюємо марку і модель
        self.make = Make.objects.create(name='Toyota')
        self.model = CarModel.objects.create(name='Camry', make=self.make)

        # Створюємо продавця з Basic акаунтом
        self.seller = CustomUser.objects.create_user(
            username='seller1',
            password='TestPass123!',
            role='seller',
            account_type='basic'
        )

        # Створюємо продавця з Premium акаунтом
        self.premium_seller = CustomUser.objects.create_user(
            username='premium_seller',
            password='TestPass123!',
            role='seller',
            account_type='premium'
        )

        self.cars_url = reverse('car-list-create')

        # Дані для створення оголошення
        self.car_data = {
            'make': self.make.id,
            'model': self.model.id,
            'year': 2022,
            'mileage': 10000,
            'description': 'Чудовий автомобіль',
            'price': '20000.00',
            'currency': 'USD',
            'city': 'Kyiv',
            'region': 'Kyiv oblast'
        }

    def test_basic_seller_can_create_one_listing(self):
        """Basic продавець може створити одне оголошення"""
        self.client.force_authenticate(user=self.seller)
        response = self.client.post(self.cars_url, self.car_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_basic_seller_cannot_create_two_listings(self):
        """Basic продавець не може створити два оголошення"""
        self.client.force_authenticate(user=self.seller)

        # Створюємо перше оголошення вручну зі статусом active
        Car.objects.create(
            owner=self.seller,
            make=self.make,
            model=self.model,
            year=2020,
            price=15000,
            currency='USD',
            status='active'
        )

        # Спробуємо створити друге
        response = self.client.post(self.cars_url, self.car_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_premium_seller_can_create_multiple_listings(self):
        """Premium продавець може створити необмежену кількість оголошень"""
        self.client.force_authenticate(user=self.premium_seller)

        # Створюємо перше оголошення
        response1 = self.client.post(self.cars_url, self.car_data)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        # Створюємо друге оголошення
        response2 = self.client.post(self.cars_url, self.car_data)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

    def test_buyer_cannot_create_listing(self):
        """Покупець не може створити оголошення"""
        buyer = CustomUser.objects.create_user(
            username='buyer1',
            password='TestPass123!',
            role='buyer'
        )
        self.client.force_authenticate(user=buyer)
        response = self.client.post(self.cars_url, self.car_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_cannot_create_listing(self):
        """Неавторизований користувач не може створити оголошення"""
        response = self.client.post(self.cars_url, self.car_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_anyone_can_view_listings(self):
        """Будь-хто може переглядати активні оголошення"""
        # Не авторизуємось
        response = self.client.get(self.cars_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)