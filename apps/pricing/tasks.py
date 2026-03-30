from celery import shared_task
from .services import fetch_rates_from_privatbank


@shared_task
def update_exchange_rates():
    """
    Щоденна задача — оновлює курси валют з ПриватБанку.
    Запускається автоматично о 9:00 кожного дня.
    """
    print('[Celery] Оновлення курсів валют...')
    rates = fetch_rates_from_privatbank()

    if rates:
        print(f'[Celery] Курси оновлено: {rates}')
        return {'status': 'success', 'rates': {k: str(v) for k, v in rates.items()}}
    else:
        print('[Celery] Помилка оновлення курсів')
        return {'status': 'error'}