"""
Django settings for my_fossil project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

BASE_URL = 'localhost:8000'

STATIC_URL = '/static/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6jdo5k9(!ctw6a!_s@0@6^-90@oq^n7wh&f_6&%_0uou%i=yi5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'fossil_app',
    'db_orm',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'my_fossil.template_loaders.App_Directoriesloader',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'my_fossil.middlewares.DatabaseMiddleware',
)

ROOT_URLCONF = 'my_fossil.urls'

WSGI_APPLICATION = 'my_fossil.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
#}

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

_MAIN_ENGINE = create_engine(
    URL(
        drivername='mysql',
        username='will',
        password='will1234',
        host='localhost',
        port=3306,
        database='fossil',
    ),
    connect_args={'charset':'utf8'},
    pool_recycle=True,
    echo=False,
)

MAIN_SESSION_OPTIONS = {
    'bind': _MAIN_ENGINE,
    'autoflush': False,
    'autocommit': False,
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
