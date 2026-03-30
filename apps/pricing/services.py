import requests
from decimal import Decimal
from datetime import date
from .models import ExchangeRate


def fetch_rates_from_privatbank():
    """
    Отримує курси валют з API ПриватБанку і зберігає в БД.
    ПриватБанк повертає курси для всіх валют — ми беремо тільки USD і EUR.
    """
    url = 'https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5'

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # кидає помилку якщо статус не 200
        data = response.json()
    except requests.RequestException as e:
        print(f'Помилка отримання курсів: {e}')
        return None

    today = date.today()
    rates = {}

    for item in data:
        currency = item.get('ccy')  # назва валюти: USD, EUR тощо
        if currency in ['USD', 'EUR']:
            rate = Decimal(str(item.get('sale', 0)))  # курс продажу

            # Зберігаємо або оновлюємо курс на сьогодні
            obj, created = ExchangeRate.objects.update_or_create(
                currency=currency,
                date=today,
                defaults={'rate_to_uah': rate}
            )
            rates[currency] = rate

    return rates


def get_today_rates():
    """
    Повертає сьогоднішні курси з БД.
    Якщо курсів немає — завантажує їх з ПриватБанку.
    """
    today = date.today()
    rates = {}

    for currency in ['USD', 'EUR']:
        try:
            rate_obj = ExchangeRate.objects.get(currency=currency, date=today)
            rates[currency] = rate_obj.rate_to_uah
        except ExchangeRate.DoesNotExist:
            # Курсів немає в БД — завантажуємо
            fetched = fetch_rates_from_privatbank()
            if fetched:
                rates = fetched
            break

    return rates


def convert_price(price, currency, rates):
    """
    Конвертує ціну в усі три валюти.

    price — оригінальна ціна
    currency — оригінальна валюта (USD, EUR або UAH)
    rates — словник {'USD': Decimal(...), 'EUR': Decimal(...)}

    Повертає словник з цінами в усіх валютах.
    """
    price = Decimal(str(price))
    usd_rate = rates.get('USD', Decimal('40'))  # fallback якщо API недоступний
    eur_rate = rates.get('EUR', Decimal('43'))

    if currency == 'USD':
        price_usd = price
        price_uah = price * usd_rate
        price_eur = price_uah / eur_rate

    elif currency == 'EUR':
        price_eur = price
        price_uah = price * eur_rate
        price_usd = price_uah / usd_rate

    elif currency == 'UAH':
        price_uah = price
        price_usd = price / usd_rate
        price_eur = price / eur_rate

    else:
        return {}

    return {
        'price_usd': round(price_usd, 2),
        'price_eur': round(price_eur, 2),
        'price_uah': round(price_uah, 2),
        'exchange_rate_used': usd_rate,
    }