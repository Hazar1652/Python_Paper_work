import os
from celery import Celery

# Вказуємо Django які налаштування використовувати
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

# Створюємо екземпляр Celery
app = Celery('autoria')

# Читаємо конфігурацію Celery з Django settings
# namespace='CELERY' означає що всі Celery налаштування
# в settings.py починаються з CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматично знаходить tasks.py у всіх INSTALLED_APPS
app.autodiscover_tasks()