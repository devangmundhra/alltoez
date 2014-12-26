from alltoez.configs.common.settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
PROJECT_DOMAIN = "http://alltoez.alltoez.co.uk"

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'alltoez',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
    }
}

# Project settings and active names
PROJECT_SITE_DOMAIN = 'alltoez.com'
GOOGLE_MAPS_API_KEY = "AIzaSyBg7rZjToQyi9izk13QfLegTueVEuWxfa0"

# Caching
CACHE_BACKEND = 'johnny.backends.memcached://127.0.0.1:11211'

# If you want to use Django Debug Toolbar, you need to list your IP address here
INTERNAL_IPS = ('0.0.0.0')

# Email addresses
MANAGERS = (
    ('Devang Mundhra', 'devangmundhra@gmail.com'),
)

# logging
import logging.config
LOG_FILENAME = os.path.join(os.path.dirname(__file__), 'logging.conf')
logging.config.fileConfig(LOG_FILENAME)

DJANGO_STATIC = not DEBUG
DJANGO_STATIC_SAVE_PREFIX = os.path.join(MEDIA_ROOT, 'cache-forever')
DJANGO_STATIC_NAME_PREFIX = "cache-forever/"
if DEBUG:
    DJANGO_STATIC_MEDIA_URL = STATIC_URL
else:
    DJANGO_STATIC_MEDIA_URL = MEDIA_URL
DJANGO_STATIC_MEDIA_URL_ALWAYS = True
DJANGO_STATIC_MEDIA_ROOTS = [os.path.join(SITE_ROOT, 'apps/common/static'), STATIC_ROOT, MEDIA_ROOT]
