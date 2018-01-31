from .base import *

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases




DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3',
        'NAME': os.path.join(BASE_DIR,'../../data/olimpia/followingseries.sqlite3'),
    }
}
LOGS_PATH=os.path.join(BASE_DIR, '../../logs/olimpia')

# SECURITY WARNING: don't run with DEBUG turned on in production!
DEBUG = True

# ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['davidperezmillan.zapto.org','nonave.com']

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
        'plugins_files': {
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGS_PATH,'plugins.log'),
            'maxBytes': 1024*1024*2, # 2 MB
            'backupCount': 5,
            'formatter':'standard',
        },
        'daily_files': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOGS_PATH,'daily.log'),
            'when': 'D', # this specifies the interval
            'interval': 1, # defaults to 1, only necessary for other values 
            'backupCount': 10, # how many backup file to keep, 10 days
            'formatter':'report_daily',
        },
        'cron_files': {
            'class':'logging.handlers.RotatingFileHandler',
            'filename':os.path.join(LOGS_PATH,'olimpiacronjobs.log'),
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
            'filename': os.path.join(LOGS_PATH,'merc.log'),
            'maxBytes': 1024*1024*2, # 2 MB
            'backupCount': 5,
            'formatter':'standard',
        },
        'general_error': {
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGS_PATH,'merc_error.log'),
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
        'merc': {
            'handlers': ['general_error'],
            'level': 'WARN',
        },
        'daily': {
            'handlers': ['daily_files'],
            'level': 'INFO',
        },
        'merc.at.plugins': {
            'handlers': ['plugins_files'],
            'level': 'INFO',
            'propagate': False,
        },
        'merc.management.commands': {
            'handlers': ['cron_files'],
            'level': 'INFO',
        },
    }
}