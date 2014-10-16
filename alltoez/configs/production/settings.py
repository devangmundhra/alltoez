from alltoez.configs.common.settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG
PROJECT_DOMAIN = "http://alltoez.com"

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
import os
import logging.config
LOG_FILENAME = os.path.join(os.path.dirname(__file__), 'logging.conf')
logging.config.fileConfig(LOG_FILENAME)

#email config
DEFAULT_FROM_EMAIL = 'postmaster@sandboxe9f734d40d854192ac1344226e7b5125.mailgun.org'
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'postmaster@sandboxe9f734d40d854192ac1344226e7b5125.mailgun.org'
EMAIL_HOST_PASSWORD = '3c8af3c9310cbde4d2e43b3e66e07948'
