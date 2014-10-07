from alltoez.configs.common.settings import *

DEBUG = True
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

ADMINS = (('Raw Jam Dev', 'dev@rawjam.co.uk')),
MANAGERS = ('Raw Jam Dev', 'dev@rawjam.co.uk'),

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
