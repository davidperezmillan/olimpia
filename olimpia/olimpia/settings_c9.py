import os, sys

from settings import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3',
        'NAME': os.path.join(BASE_DIR,'../data/olimpia/c9.sqlite3'),
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
        'airtrap_files': {
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGS_PATH,'c9_at.log'),
            'maxBytes': 1024*1024*2, # 2 MB
            'backupCount': 5,
            'formatter':'standard',
        },
        'cron_files': {
            'class':'logging.handlers.RotatingFileHandler',
            'filename':os.path.join(LOGS_PATH,'c9_olimpiacronjobs.log'),
            'maxBytes': 1024*1024*2, # 2 MB
            'backupCount': 5,
            'formatter':'standard',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter':'standard',
        },
        'general': {
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGS_PATH,'c9_merc.log'),
            'maxBytes': 1024*1024*2, # 2 MB
            'backupCount': 5,
            'formatter':'standard',
        },
    },
    'loggers': {
        'merc': {
            'handlers': ['console','general'],
            'level': 'DEBUG',
        },
        'hod': {
            'handlers': ['console',],
            'level': 'DEBUG',
        },
        'merc.at': {
            'handlers': ['airtrap_files'],
            'level': 'INFO',
            
        },
        'merc.management.commands': {
            'handlers': ['cron_files'],
            'level': 'INFO',
        },
        'hod.management.commands': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}