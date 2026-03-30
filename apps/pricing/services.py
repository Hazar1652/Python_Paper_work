import requests
from decimal import Decimal
from datetime import date
from .models import ExchangeRate


def fetch_rates_from_privatbank():

    url = 'https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5'

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f'Помилка отримання курсів: {e}')
        return None

    today = date.today()
    rates = {}

    for item in data:
        currency = item.get('ccy')
        if currency in ['USD', 'EUR']:
            rate = Decimal(str(item.get('sale', 0)))


            obj, created = ExchangeRate.objects.update_or_create(
                currency=currency,
                date=today,
                defaults={'rate_to_uah': rate}
            )
            rates[currency] = rate

    return rates


def get_today_rates():

    today = date.today()
    rates = {}

    for currency in ['USD', 'EUR']:
        try:
            rate_obj = ExchangeRate.objects.get(currency=currency, date=today)
            rates[currency] = rate_obj.rate_to_uah
        except ExchangeRate.DoesNotExist:
            fetched = fetch_rates_from_privatbank()
            if fetched:
                rates = fetched
            break

    return rates


def convert_price(price, currency, rates):

    price = Decimal(str(price))
    usd_rate = rates.get('USD', Decimal('40'))
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