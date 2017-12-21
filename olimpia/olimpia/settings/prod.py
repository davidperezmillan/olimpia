from .base import *

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] - %(name)s - %(filename)s:%(lineno)d - %(message)s'
        },
        'standard_alt':{
            'format' : '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        }
    },
    'handlers': {
        # 'hermes_django': {
        #     'level':'DEBUG',
        #     'class':'logging.handlers.RotatingFileHandler',
        #     'filename': 'logs/hermes_django.log',
        #     'maxBytes': 1024*1024*5, # 5 MB
        #     'backupCount': 5,
        #     'formatter':'standard',
        # },  
        'plugins_files': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': 'logs/merc/plugins.log',
            'maxBytes': 1024*1024*2, # 2 MB
            'backupCount': 5,
            'formatter':'standard',
        },
        'cron_files': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': 'logs/merc/olimpiacronjobs.log',
            'maxBytes': 1024*1024*2, # 2 MB
            'backupCount': 5,
            'formatter':'standard',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter':'standard',
        }
    },
    'loggers': {
        'merc': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'merc.at.plugins': {
            'handlers': ['plugins_files'],
            'level': 'INFO',
            'propagate': False,
        },
        'merc.management.commands': {
            'handlers': ['cron_files'],
            'level': 'DEBUG',
            'propagate': False,
        },
        # 'hermes_django': {
        #     'handlers': ['console', 'hermes_django'],
        #     'level': 'DEBUG',
        # },
        # 'django.request': {
        #     'handlers': ['console', 'request_handler'],
        #     'propagate': False,
        #     'level': 'DEBUG'
        # }
    }
}



