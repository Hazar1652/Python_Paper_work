from .base import *

# На локалці DEBUG=True — показує детальні помилки
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# CORS — дозволяємо React (порт 3000) звертатись до API (порт 8000)
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
]
import sys
if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'autoria',
            'USER': 'autoria_user',
            'PASSWORD': 'autoria_pass',
            'HOST': 'db',
            'PORT': '5432',
        }
    }