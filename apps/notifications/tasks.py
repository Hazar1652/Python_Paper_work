from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_moderation_notification(manager_email, car_id, reason):

    print(f'[Celery] Відправка email до {manager_email} про оголошення #{car_id}')

    subject = f'Оголошення #{car_id} деактивовано'
    message = (
        f'Оголошення #{car_id} було автоматично деактивовано.\n'
        f'Причина: {reason}\n\n'
        f'Будь ласка, перевірте оголошення в адмін панелі.'
    )

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[manager_email],
            fail_silently=False,
        )
        print(f'[Celery] Email відправлено до {manager_email}')
        return {'status': 'sent', 'email': manager_email}
    except Exception as e:
        print(f'[Celery] Помилка відправки email: {e}')
        return {'status': 'error', 'error': str(e)}


@shared_task
def send_listing_flagged_notification(seller_email, car_id, edits_remaining):

    print(f'[Celery] Сповіщення продавця {seller_email} про flagged оголошення #{car_id}')

    subject = f'Ваше оголошення #{car_id} потребує виправлення'
    message = (
        f'Ваше оголошення #{car_id} містить недозволений контент.\n'
        f'У вас залишилось {edits_remaining} спроб для виправлення.\n\n'
        f'Будь ласка, відредагуйте оголошення і видаліть недозволені слова.'
    )

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[seller_email],
            fail_silently=False,
        )
        return {'status': 'sent'}
    except Exception as e:
        return {'status': 'error', 'error': str(e)}