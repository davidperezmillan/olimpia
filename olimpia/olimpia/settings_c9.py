import os, sys

from settings import *

LOGS_PATH=os.path.join(BASE_DIR, '../logs/olimpia')

# SECURITY WARNING: don't run with DEBUG turned on in production!
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../data/olimpia/c9.sqlite3'),
    }
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] - %(name)s - %(filename)s:%(lineno)d - %(message)s'
        },
        'standard_alt':{
            'format' : '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'report_daily': {
            'format' : '%(asctime)s: %(message)s',
            'datefmt' : '%d-%m-%Y %H:%M'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter':'standard',
        },
        'general': {
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGS_PATH,'hoor.log'),
            'maxBytes': 1024*1024*2, # 2 MB
            'backupCount': 5,
            'formatter':'standard',
        },
    },
    'loggers': {
        'hoor': {
            'handlers': ['console','general'],
            'level': 'DEBUG',
        },
    }
}