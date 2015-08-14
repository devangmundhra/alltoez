import keen

from .base import *

DATABASES = {'default': dj_database_url.config()}
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'

DEBUG = True
TEMPLATE_DEBUG = DEBUG
TASTYPIE_FULL_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG

SITE_ID = 1

# Haystack configuration
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
        'INCLUDE_SPELLING': True,
    },
}

# Root address of our site
ROOT = 'http://127.0.0.1:5000'

# Celery configurations
BROKER_URL = 'redis://'
CELERY_RESULT_BACKEND = BROKER_URL
CELERY_SEND_TASK_ERROR_EMAILS = False
CELERY_ALWAYS_EAGER = True

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost'
]
INTERNAL_IPS = ALLOWED_HOSTS

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

CACHEOPS_REDIS = {
    'host': REDIS_ENDPOINT, # redis-server is on same machine
    'port': 6379,        # default redis port
    'db': 0,             # TODO: SELECT non-default redis database
                         # using separate redis db or redis instance
                         # is highly recommended
    'socket_timeout': 3,
}

# No logging in development
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        # Might as well log any errors anywhere else in Django
        '': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
    }
}
#email config
# EMAIL_BACKEND = 'djrill.mail.backends.djrill.DjrillBackend'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


STATIC_FILES_BUCKET = 'alltoezstatic-dev'
STATIC_S3_DOMAIN = '%s.s3.amazonaws.com' % STATIC_FILES_BUCKET
STATIC_URL = "https://%s/" % STATIC_S3_DOMAIN

MEDIA_FILES_BUCKET = 'alltoez-dev'
MEDIA_S3_DOMAIN = '%s.s3.amazonaws.com' % MEDIA_FILES_BUCKET
# MEDIA_URL = "https://%s/" % MEDIA_S3_DOMAIN
MEDIA_URL = "http://d4fn4xyggcxct.cloudfront.net/"

AWS_STORAGE_BUCKET_NAME = MEDIA_FILES_BUCKET
AWS_S3_CUSTOM_DOMAIN = MEDIA_S3_DOMAIN

NEW_RELIC_ENVIRONMENT ='development'
PIO_ACCESS_KEY = 'KQJk2aYAaKzIayZVBqSEC4NmdxMUXGxN3RsUQ4IxsbC8qGW2aHBQSZakT8eIoCzW'
PIO_ENGINE_ENDPOINT = 'http://127.0.0.1:8001'
PIO_EVENT_SERVER_ENDPOINT = 'http://127.0.0.1:7070'
FACEBOOK_APP_ID ="436853689787509"
FLICKR_API_KEY = '8213780dead35d871cd1a9f5a07e8401'
GOOGLE_API_KEY = 'AIzaSyCtXH8YMLGjSlnqnX4Pf1_M_yWsiOW8szU'
GOOGLE_SENGINE_ID = '015946843765970452323:8ogczsyyuiq'
AWS_ACCESS_KEY_ID = 'AKIAIAYKKFWN5ENO6BXA'
AWS_SECRET_ACCESS_KEY = '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'
GOOGLE_MAPS_V3_APIKEY = GOOGLE_API_KEY

# Static files
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'

keen.project_id = "55c87ab059949a484b7401e0"
keen.write_key = "2511b67352eb6dda35ba69b1a6d5d72d85635abcdfea8064addd01ea89a4401f8f41a73db2aff56e4684a047922ae15c50a8e02f95fc9c0d6f67d99f8b95381c688d03f2d25f8f900936003aba9beecdf538cfafdb59b645c76b19825ca22fcca6a2d211b332a6ebc628f51a13360875"
keen.read_key = "81b640e0a7bd327de3def5ee38e7a611631f5fec9ef51ffde31dc2eaf01a5afb44ada23f47ff093a378b02dd085cdca4c8bd1c6208d23cbd39ee3cb0ce41d0ad8c2df488844c9854bc131c4ecfcf4e0490ced94f8c81438c4c22f2194eefa9866b74ff2504d37a1c1d1c43c835bb94e6"
keen.master_key = "CEF087C1E8CE4E3848A5E0890D30698D"

