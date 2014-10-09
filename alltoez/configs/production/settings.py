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

ADMINS = (('Devang', 'devangmundhra@gmail.com')),
MANAGERS = ('Devang', 'devangmundhra@gmail.com'),

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
