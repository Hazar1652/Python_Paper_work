from django.test import TestCase
from decimal import Decimal
from unittest.mock import patch, MagicMock
from .services import convert_price, get_today_rates, fetch_rates_from_privatbank


class CurrencyConversionTest(TestCase):
    def setUp(self):
        self.rates = {
            'USD': Decimal('40.00'),
            'EUR': Decimal('43.00'),
        }

    def test_convert_from_usd(self):
        result = convert_price('1000', 'USD', self.rates)
        self.assertEqual(result['price_usd'], Decimal('1000'))
        self.assertEqual(result['price_uah'], Decimal('40000.00'))
        self.assertAlmostEqual(float(result['price_eur']), 930.23, places=1)

    def test_convert_from_eur(self):
        result = convert_price('1000', 'EUR', self.rates)
        self.assertEqual(result['price_eur'], Decimal('1000'))
        self.assertEqual(result['price_uah'], Decimal('43000.00'))

    def test_convert_from_uah(self):
        result = convert_price('40000', 'UAH', self.rates)
        self.assertEqual(result['price_uah'], Decimal('40000'))
        self.assertEqual(result['price_usd'], Decimal('1000.00'))

    def test_invalid_currency(self):
        result = convert_price('1000', 'GBP', self.rates)
        self.assertEqual(result, {})

    def test_exchange_rate_saved(self):
        result = convert_price('1000', 'USD', self.rates)
        self.assertEqual(result['exchange_rate_used'], Decimal('40.00'))


class PrivatBankAPITest(TestCase):
    @patch('apps.pricing.services.requests.get')
    def test_fetch_rates_success(self, mock_get):
        """
        @patch замінює реальний requests.get на підробку
        Тест не робить реальний HTTP запит до ПриватБанку
        """
        # Налаштовуємо що поверне підроблений requests.get
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {'ccy': 'USD', 'base_ccy': 'UAH', 'buy': '39.50', 'sale': '40.00'},
            {'ccy': 'EUR', 'base_ccy': 'UAH', 'buy': '42.50', 'sale': '43.00'},
        ]
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        # Викликаємо функцію
        result = fetch_rates_from_privatbank()

        # Перевіряємо результат
        self.assertIn('USD', result)
        self.assertIn('EUR', result)
        self.assertEqual(result['USD'], Decimal('40.00'))
        self.assertEqual(result['EUR'], Decimal('43.00'))

        # Перевіряємо що requests.get був викликаний з правильним URL
        mock_get.assert_called_once_with(
            'https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5',
            timeout=10
        )

    @patch('apps.pricing.services.requests.get')
    def test_fetch_rates_api_failure(self, mock_get):
        """
        Тест перевіряє що функція правильно обробляє помилку API
        """
        import requests
        mock_get.side_effect = requests.RequestException('API недоступний')

        result = fetch_rates_from_privatbank()

        # При помилці функція повертає None
        self.assertIsNone(result)

    @patch('apps.pricing.services.fetch_rates_from_privatbank')
    def test_get_today_rates_uses_mock(self, mock_fetch):
        """
        Тест get_today_rates з замоканим ПриватБанком
        """
        mock_fetch.return_value = {
            'USD': Decimal('40.00'),
            'EUR': Decimal('43.00'),
        }

        rates = get_today_rates()

        self.assertIn('USD', rates)
        self.assertIn('EUR', rates)