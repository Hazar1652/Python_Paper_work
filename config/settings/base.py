import environ
import os
from pathlib import Path

# BASE_DIR — це корінь проєкту (папка де лежить manage.py)
# __file__ — це поточний файл (base.py)
# .resolve() — отримує повний шлях
# .parent.parent.parent — піднімаємось на 3 рівні вгору:
#   base.py → settings/ → config/ → корінь проєкту
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Ініціалізуємо django-environ — він читає наш .env файл
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Секретний ключ Django — береться з .env файлу
SECRET_KEY = env('SECRET_KEY')

# INSTALLED_APPS — список всіх додатків які Django завантажує
INSTALLED_APPS = [
    # Стандартні Django додатки
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Сторонні пакети
    'rest_framework',           # DRF — інструменти для API
    'rest_framework_simplejwt', # JWT токени для авторизації
    'corsheaders',
    'drf_spectacular',# Дозволяє React звертатись до API

    # Наші додатки (поки порожні, будемо заповнювати)
    'apps.users',
    'apps.roles',
    'apps.cars',
    'apps.pricing',
    'apps.moderation',
    'apps.stats',
    'apps.notifications',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS — має бути якомога вище
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# База даних — читає DATABASE_URL з .env
# Наприклад: postgres://user:pass@db:5432/autoria
DATABASES = {
    'default': env.db('DATABASE_URL')
}

# Наша кастомна модель користувача (створимо в кроці 3)
AUTH_USER_MODEL = 'users.CustomUser'

# Валідатори паролів
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Kyiv'
USE_I18N = True
USE_TZ = True

# Статичні файли (CSS, JS)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Медіа файли (фото автомобілів)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# DRF — налаштування Django REST Framework
REST_FRAMEWORK = {
    # За замовчуванням всі endpoints вимагають авторизації
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# Redis — для кешування і Celery
REDIS_URL = env('REDIS_URL')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': REDIS_URL,
    }
}

# Celery — черга задач
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
# Email налаштування
# В розробці — виводимо emails в консоль замість реальної відправки
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@autoria.com'
from celery.schedules import crontab

# Celery Beat — розклад автоматичних задач
CELERY_BEAT_SCHEDULE = {
    'update-exchange-rates-daily': {
        'task': 'apps.pricing.tasks.update_exchange_rates',
        # Запускати щодня о 9:00
        'schedule': crontab(hour=9, minute=0),
    },
}
# Налаштування drf-spectacular (Swagger)
SPECTACULAR_SETTINGS = {
    'TITLE': 'AutoRIA Clone API',
    'DESCRIPTION': 'Документація для сервісу продажу автомобілів та управління курсами валют',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # Це дозволить групувати методи за назвами додатків
    'SCHEMA_PATH_PREFIX': r'/api/v[0-9]/',
}