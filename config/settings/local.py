from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

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