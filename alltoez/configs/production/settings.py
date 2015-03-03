from configs.common.settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG
PROJECT_DOMAIN = "http://www.alltoez.com"

SITE_ID = 2

WSGI_APPLICATION = 'alltoez.configs.production.wsgi.application'
# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'alltoez',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
    }
}

# Haystack configuration
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'https://k0995adg9h:fjrnpz1k2k@alltoez-7040390127.us-west-2.bonsai.io',
        'INDEX_NAME': 'haystack',
        'INCLUDE_SPELLING': True,
    },
}

ADMINS = (('Devang Mundhra', 'devangmundhra@gmail.com'), ('Ruchika Damani', 'ruchikadamani90@gmail.com')),
MANAGERS = ('Devang Mundhra', 'devangmundhra@gmail.com'), ('Ruchika Damani', 'ruchikadamani90@gmail.com'),

ALLOWED_HOSTS = [
    '.alltoez.com',
]

PIPELINE_ENABLED = not DEBUG

"""
STATICFILES_STORAGE = 'apps.alltoez.storage.S3PipelineStorage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = 'AKIAJRVBYWEHDQIOFG2A'
AWS_SECRET_ACCESS_KEY = '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'

STATIC_FILES_BUCKET = 'alltoezstatic'
STATIC_S3_DOMAIN = '%s.s3.amazonaws.com' % STATIC_FILES_BUCKET
STATIC_URL = "https://%s/" % STATIC_S3_DOMAIN

MEDIA_FILES_BUCKET = 'alltoez'
MEDIA_S3_DOMAIN = '%s.s3.amazonaws.com' % MEDIA_FILES_BUCKET
MEDIA_URL = "https://%s/" % MEDIA_S3_DOMAIN

AWS_STORAGE_BUCKET_NAME = MEDIA_FILES_BUCKET
AWS_S3_CUSTOM_DOMAIN = MEDIA_S3_DOMAIN
"""

GOOGLE_ANALYTICS_CODE = "UA-55773544-1"
FACEBOOK_APP_ID = '869081253104828'

REDIS_ENDPOINT = '127.0.0.1'

#  Caching related parameters
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        "LOCATION": "redis://%s:6379/1" % REDIS_ENDPOINT,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

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
MANDRILL_API_KEY = 'iA4W9WiP9CT7R3FwyQmc3A'
EMAIL_BACKEND = 'djrill.mail.backends.djrill.DjrillBackend'

# PredictionIO settings
PIO_ACCESS_KEY = 'YW9d0Wq3l7QgzNVisiXXFOFtMDiJR1TJOCp2QFNqVcpcSsvkC38O0TiAefdZq37Z'
PIO_ENGINE_ENDPOINT = 'http://54.197.245.21:8000'
PIO_EVENT_SERVER_ENDPOINT = 'http://54.197.245.21:7070'