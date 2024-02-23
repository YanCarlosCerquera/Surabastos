from .base import *
import os
# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dbsurabastosv2',
        'USER': 'surabastos',
        'PASSWORD': '60402yancerquera',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = 'media/'

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'applications/RegistroUsuarios', 'static'),
    os.path.join(BASE_DIR, 'applications/Blog', 'static'),
    os.path.join(BASE_DIR, 'applications/Perfiles', 'static')
]