"""
Django settings for ERP project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
import environ
import mimetypes

mimetypes.add_type("text/css", ".css", True)
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-%zeh278!iyh%*gfum_di436#vm_vs5j-j#(*$+#h!ctf4h%%3#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '192.168.88.98', 'office.obs-balashiha.ru']

env = environ.Env()
environ.Env.read_env('.env')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'crispy_forms',
    "crispy_bootstrap5",
    'apps.core',
    'apps.reports',
    'widget_tweaks',
    'sass_processor',
    'import_export',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CRISPY_TEMPLATE_PACK = 'bootstrap5'

ROOT_URLCONF = 'ERP.urls'

AUTH_USER_MODEL = 'core.ErpUser'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.core.context_core.notification_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'ERP.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env("POSTGRES_DB"),
        'USER': env("POSTGRES_USER"),
        'PASSWORD': env("POSTGRES_PASSWORD"),
        'HOST': env("POSTGRES_HOST"),
        'PORT': env("POSTGRES_PORT"),
        'CONN_MAX_AGE': 60 * 10,  # 10 minutes
    }
}


caches = {
    "default": {
        "backend": "django_redis.cache.rediscache",
        "location": "redis://redis-server:6379",
        "options": {
            "client_class": "django_redis.client.defaultclient",
        }
    }
}

COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
]

COMPRESS_JS_FILTERS = [
    'compressor.filters.jsmin.JSMinFilter',
]

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_CACHE_ALIAS = 'default'

SESSION_COOKIE_AGE = 1209600  # Время жизни сессии в секундах (2 недели по умолчанию)
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

CELERY_BROKER_URL = 'redis://redis-server:6379'
CELERY_RESULT_BACKEND = 'redis://redis-server:6379'
CELERY_TIMEZONE = 'Europe/Moscow'
USE_TZ = True
CELERY_TASK_TRACK_STARTED = True
CELERY_IMPORTS = ['web.tasks']

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

FIRST_DAY_OF_WEEK = 1
DATE_INPUT_FORMATS = ['%d.%m.%Y', ]
TIME_INPUT_FORMATS = ['%H:%M', ]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
]

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'apps/static'

SASS_PROCESSOR_ROOT = BASE_DIR / 'static'

STATICFILES_DIRS = (
    (BASE_DIR / 'static'),
)

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
