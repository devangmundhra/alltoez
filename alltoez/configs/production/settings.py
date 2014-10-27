from alltoez.configs.common.settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG
PROJECT_DOMAIN = "http://alltoez.com"

SITE_ID = 2

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'alltoez',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
    }
}

ADMINS = (('Devang Mundhra', 'devangmundhra@gmail.com')),
MANAGERS = ('Devang Mundhra', 'devangmundhra@gmail.com'),

ALLOWED_HOSTS = [
    '.alltoez.com',
]

PIPELINE_ENABLED = not DEBUG
PIPELINE_CSS = {
    'theme': {
        'source_filenames': (
            'css/chosen.css',
            'less/theme.less' if not DEBUG else ''
        ),
        'output_filename': 'css/theme.min.css',
        'variant': 'datauri'
    },
}

GOOGLE_ANALYTICS_CODE = "UA-55773544-1"

# logging
# import os
# import logging.config
# LOG_FILENAME = os.path.join(os.path.dirname(__file__), 'logging.conf')
# logging.config.fileConfig(LOG_FILENAME)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
         'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        },
    }
}

# celery config
CELERY_SEND_TASK_ERROR_EMAILS = True

#email config
DEFAULT_FROM_EMAIL = 'Postmaster <postmaster@alltoez.com>'
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'postmaster@alltoez.com'
EMAIL_HOST_PASSWORD = 'f23194b06f816adc5b5e6f235ed33ff1'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'