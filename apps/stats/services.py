from django.core.cache import cache
from django.utils import timezone
from apps.cars.models import Car
from decimal import Decimal


def get_view_keys(car_id):

    now = timezone.now()

    # Формат ключів: car_views:<car_id>:<period>:<date>
    day_key = f'car_views:{car_id}:day:{now.strftime("%Y-%m-%d")}'
    week_key = f'car_views:{car_id}:week:{now.strftime("%Y-W%W")}'
    month_key = f'car_views:{car_id}:month:{now.strftime("%Y-%m")}'
    total_key = f'car_views:{car_id}:total'

    return {
        'day': day_key,
        'week': week_key,
        'month': month_key,
        'total': total_key,
    }


def record_view(car_id):

    keys = get_view_keys(car_id)


    cache.incr(keys['total']) if cache.get(keys['total']) else cache.set(keys['total'], 1)


    if cache.get(keys['day']):
        cache.incr(keys['day'])
    else:
        cache.set(keys['day'], 1, timeout=60 * 60 * 25)

    if cache.get(keys['week']):
        cache.incr(keys['week'])
    else:
        cache.set(keys['week'], 1, timeout=60 * 60 * 24 * 8)

    # Місячний лічильник живе 32 дні
    if cache.get(keys['month']):
        cache.incr(keys['month'])
    else:
        cache.set(keys['month'], 1, timeout=60 * 60 * 24 * 32)


def get_view_stats(car_id):

    keys = get_view_keys(car_id)

    return {
        'total': cache.get(keys['total']) or 0,
        'today': cache.get(keys['day']) or 0,
        'this_week': cache.get(keys['week']) or 0,
        'this_month': cache.get(keys['month']) or 0,
    }


def get_price_stats(car_id):

    try:
        car = Car.objects.get(id=car_id)
    except Car.DoesNotExist:
        return {}

    similar_cars = Car.objects.filter(
        make=car.make,
        model=car.model,
        status='active',
    ).exclude(id=car_id)

    regional_cars = similar_cars.filter(region=car.region)
    regional_prices = [c.price_usd for c in regional_cars if c.price_usd]
    avg_regional = (
        sum(regional_prices) / len(regional_prices)
        if regional_prices else None
    )

    national_prices = [c.price_usd for c in similar_cars if c.price_usd]
    avg_national = (
        sum(national_prices) / len(national_prices)
        if national_prices else None
    )

    return {
        'your_price_usd': float(car.price_usd) if car.price_usd else None,
        'avg_price_regional_usd': float(round(avg_regional, 2)) if avg_regional else None,
        'avg_price_national_usd': float(round(avg_national, 2)) if avg_national else None,
        'region': car.region,
        'similar_cars_count': similar_cars.count(),
    }