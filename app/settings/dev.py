import sys

from .base import INSTALLED_APPS, MIDDLEWARE


# Security

DEBUG = True


# debug toolbar

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_COLLAPSED': True,
    'SHOW_TOOLBAR_CALLBACK': 'app.settings.helpers.show_toolbar',
}

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]


# auth

AUTH_PASSWORD_VALIDATORS = []


# email

EMAIL_USE_TLS = False


# static

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'


# files

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'


# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detail': {
            'format': (
                '%(levelname)s %(asctime)s %(pathname)s:%(lineno)s '
                '[%(funcName)s] %(message)s')
        }
    },
    'handlers': {
        'stdout': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'detail',
            'stream': sys.stdout
        }
    },
    'loggers': {
        'django': {
            'handlers': ['stdout'],
            'level': 'INFO',
        }
    }
}
