"""
Django settings for olimpia project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os, sys
# import constantes as cons
# Importamos las constantes de airtrap

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# print os.path.join(BASE_DIR, '../airtrap/utilities')
sys.path.insert(0, os.path.join(BASE_DIR, '../airtrap/utilities'))
import constantes as cons

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'aa2mbm^ca*8a^lmr88p*k6dmusbod!s4t$fqa)p5nh5-tlg^k&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['davidperezmillan.zapto.org']


# Application definition

INSTALLED_APPS = [
    'mercurio.apps.MercurioConfig',
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'olimpia.urls'

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

WSGI_APPLICATION = 'olimpia.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3',
        'NAME': '{0}/conf/data/followingseries.sqlite3'.format(cons.basepath),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

STATIC_URL = '/static/'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    # 'handlers': {
    #     'hermes_django': {
    #         'level':'DEBUG',
    #         'class':'logging.handlers.RotatingFileHandler',
    #         'filename': 'logs/hermes_django.log',
    #         'maxBytes': 1024*1024*5, # 5 MB
    #         'backupCount': 5,
    #         'formatter':'standard',
    #     },  
    #     'request_handler': {
    #         'level':'DEBUG',
    #         'class':'logging.handlers.RotatingFileHandler',
    #         'filename': 'logs/django_request.log',
    #         'maxBytes': 1024*1024*5, # 5 MB
    #         'backupCount': 5,
    #         'formatter':'standard',
    #     },
    #     'console': {
    #         'level': 'DEBUG',
    #         'class': 'logging.StreamHandler',
    #         'formatter':'standard',
    #     }
    # },
    # 'loggers': {
    #     'airtrap': {
    #         'handlers': ['console'],
    #         'level': 'DEBUG',
    #     },
    #     'hermes_django': {
    #         'handlers': ['console', 'hermes_django'],
    #         'level': 'DEBUG',
    #     },
    #     'django.request': {
    #         'handlers': ['console', 'request_handler'],
    #         'propagate': False,
    #         'level': 'DEBUG'
    #     }
    # }
}
