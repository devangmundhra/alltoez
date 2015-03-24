import os, django, os.path
import logging
import urlparse
import dj_database_url
from datetime import timedelta
from django.utils.translation import ugettext_lazy as _

#-------------------------------------------------------------------------------
#	BASE SETTINGS
#-------------------------------------------------------------------------------
DEBUG = False
TEMPLATE_DEBUG = DEBUG
INTERNAL_IPS = ('127.0.0.1', 'localhost')
SECRET_KEY = '-x83)5-^cugn@*t6gh%76j@cb)zj)q7l_rm!%3=)@sw&v&d_ww'

DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
SITE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

ADMIN_MEDIA_PREFIX = "/static/admin/"
# STATIC_ROOT = os.path.join(SITE_ROOT, "static")
STATIC_ROOT = 'staticfiles'
MEDIA_ROOT = os.path.join(SITE_ROOT, "media")

PROJECT_DOMAIN = "http://www.alltoez.com"

STATIC_URL = "/static/"
"""
STATICFILES_STORAGE = 'apps.alltoez.storage.S3PipelineStorage'

STATIC_URL = "https://%s/" % STATIC_S3_DOMAIN
"""
STATIC_FILES_BUCKET = 'alltoezstatic'
STATIC_S3_DOMAIN = '%s.s3.amazonaws.com' % STATIC_FILES_BUCKET
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

MEDIA_FILES_BUCKET = 'alltoez'
MEDIA_S3_DOMAIN = '%s.s3.amazonaws.com' % MEDIA_FILES_BUCKET
# MEDIA_URL = "https://%s/" % MEDIA_S3_DOMAIN
MEDIA_URL = 'http://d1wqe2m0m7wb9o.cloudfront.net/'

AWS_STORAGE_BUCKET_NAME = MEDIA_FILES_BUCKET
AWS_S3_CUSTOM_DOMAIN = MEDIA_S3_DOMAIN
AWS_CLOUDFRONT_DOMAIN ='http://d1wqe2m0m7wb9o.cloudfront.net'
AWS_QUERYSTRING_AUTH = False

WSGI_APPLICATION = 'alltoez.wsgi.application'

ALLOWED_HOSTS = [
    '.alltoez.com',
]

ADMINS = (('Server', 'server@alltoez.com'),),
MANAGERS = ADMINS
SITE_ID = 2

# Local time
TIME_ZONE = "UTC"
LANGUAGE_CODE = "en-us"
USE_I18N = False
DATE_INPUT_FORMATS = ('%d-%m-%Y', '%Y-%m-%d')
USE_TZ = True

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
    os.path.join(PROJECT_ROOT, "alltoez", "templates")
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.CachedFileFinder',
    'pipeline.finders.PipelineFinder',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    "allauth.account.auth_backends.AuthenticationBackend",
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.media",
    'django.core.context_processors.static',
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    "apps.alltoez.context_processors.app_wide_vars",
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
)

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pipeline.middleware.MinifyHTMLMiddleware',
    'hunger.middleware.BetaMiddleware',
    'apps.alltoez.middleware.RedirectIfIncompleteProfile',
]

INSTALLED_APPS = [
    # Base Django Apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Helpful methods for admin
    'djangocms_admin_style',
    'admin_shortcuts',

    'django.contrib.admin',
    'django.contrib.sitemaps',
    'django.contrib.humanize',
    'django.contrib.gis',

    # Utilities & Helper Apps
    'filebrowser',
    'django_extensions',
    'endless_pagination',
    'pipeline',
    'location_field',
    'phonenumber_field',
    'haystack',
    'tastypie',
    'pagedown',
    'markdown_deux',
    'bootstrapform',
    'storages',
    'cacheops',
    'sorl.thumbnail',

    # Registration, Signin and Account Management
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'hunger',

    # Local Project Apps
    'apps.alltoez_profile',
    'apps.venues',
    'apps.events',
    'apps.user_actions',
    'apps.alltoez',
]

if USE_I18N:
    TEMPLATE_CONTEXT_PROCESSORS += ('django.core.context_processors.i18n',)

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

#-------------------------------------------------------------------------------
#	APP SETTINGS
#-------------------------------------------------------------------------------
DEFAULT_PROFILE_IMAGE = os.path.join(MEDIA_ROOT, 'uploads/alltoez_defaults/profile_portrait_default.png')
LANGUAGES = (
    ('en', _('English')),
)

DATABASES = {'default': dj_database_url.config()}
ROOT_URLCONF = 'alltoez.urls'
AUTH_PROFILE_MODULE = 'alltoez_profile.UserProfile'

EMAIL_SUBJECT_PREFIX = "[Alltoez Server]"
SERVER_EMAIL = 'Alltoez Server <server@alltoez.com>'
DEFAULT_FROM_EMAIL = 'Postmaster <postmaster@alltoez.com>'
EMAIL_BACKEND = 'djrill.mail.backends.djrill.DjrillBackend'

#-------------------------------------------------------------------------------
#	CACHE SETTINGS
#-------------------------------------------------------------------------------
# Caching related parameters
if 'REDISCLOUD_URL' in os.environ:
    redis_url = urlparse.urlparse(os.environ.get('REDISCLOUD_URL'))

    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': '%s:%s:0' % (redis_url.hostname, redis_url.port),
            'OPTIONS': {
                'PASSWORD': redis_url.password,
                'DB': 0,
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        }
    }

    CACHEOPS_REDIS = {
        'host': redis_url.hostname, # redis-server is on same machine
        'port': redis_url.port,        # default redis port
        'db': 0,             # TODO: SELECT non-default redis database
                             # using separate redis db or redis instance
                             # is highly recommended
        'password': redis_url.password,
        'socket_timeout': 3,
    }

CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 60
CACHE_MIDDLEWARE_KEY_PREFIX = 'alltoez:'

CACHEOPS_DEFAULTS = {
    'timeout': 60*60
}
CACHEOPS = {
    'auth.user': {'ops': 'get', 'timeout': 60*15},
    'auth.*': {'ops': ('fetch', 'get')},
    'auth.permission': {'ops': 'all'},
    '*.*': {'ops': 'all'},
}
CACHEOPS_DEGRADE_ON_FAILURE = True

#-------------------------------------------------------------------------------
#	PIPELINE SETTINGS
#-------------------------------------------------------------------------------
STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'
PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.yuglify.YuglifyCompressor'
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.yuglify.YuglifyCompressor'
PIPELINE_YUGLIFY_BINARY = os.path.join(PROJECT_ROOT, "node_modules/yuglify/bin/yuglify")
PIPELINE_COFFEE_SCRIPT_BINARY = os.path.join(PROJECT_ROOT, "node_modules/coffee-script/bin/coffee")
PIPELINE_DISABLE_WRAPPER = True
PIPELINE_COMPILERS = (
    'pipeline.compilers.less.LessCompiler',
    'pipeline.compilers.coffee.CoffeeScriptCompiler',
)
PIPELINE_LESS_BINARY = 'lessc'
PIPELINE_CSS = {
    'theme': {
        'source_filenames': (
            'css/chosen.css',
            'less/theme.less' if not DEBUG else '' #This line is giving error in collectstatic with DEBUG = True
        ),
        'output_filename': 'css/theme.min.css',
        'variant': 'datauri'
    },
}
PIPELINE_JS = {
    'base': {
        'source_filenames': (
            'js/typeahead.bundle.min.js',
            'js/main.js',
            'js/ajax_request.js',
            'js/lib/jquery.class.js',
            'js/lib/jquery.cookie.js',
            'js/lib/bootstrap.min.js',
            'js/lib/chosen.jquery.min.js',
        ),
        'output_filename': 'js/base.min.js',
    },
    'events_detail': {
        'source_filenames': (
            'js/events_ajax.coffee',
        ),
        'output_filename': 'js/events_detail.min.js',
    },
}

#-------------------------------------------------------------------------------
#	ALLAUTH SETTINGS
#-------------------------------------------------------------------------------
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = "/"

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = False
ACCOUNT_USER_DISPLAY = lambda user: user.get_full_name()
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_ADAPTER = "apps.alltoez_profile.adapter.AlltoezAccountAdapter"
SOCIALACCOUNT_ADAPTER = "apps.alltoez_profile.adapter.AlltoezSocialAccountAdapter"
SOCIALACCOUNT_ENABLED = True
SOCIALACCOUNT_PROVIDERS = {}
SOCIALACCOUNT_QUERY_EMAIL = ACCOUNT_EMAIL_REQUIRED
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_AVATAR_SUPPORT = False
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"

EMAIL_CONFIRMATION_DAYS = 5
FACEBOOK_ENABLED = True
TWITTER_ENABLED = False
OPENID_ENABLED = False

#-------------------------------------------------------------------------------
#	DJANGO-HUNGER SETTINGS
#-------------------------------------------------------------------------------
HUNGER_ENABLE = False
HUNGER_ALWAYS_ALLOW_VIEWS = [
    'apps.alltoez_profile.views.AlltoezSignupView',
    'apps.alltoez.views.home',
]
HUNGER_ALWAYS_ALLOW_MODULES = [
    'allauth.account.views',
    'allauth.socialaccount.views',
    'allauth.socialaccount.providers.oauth2.views',
    # 'apps.events.views',
    # 'apps.alltoez.views',
]

from django.core.urlresolvers import reverse_lazy
HUNGER_VERIFIED_REDIRECT = reverse_lazy('alltoez_account_signup')

#-------------------------------------------------------------------------------
#	FILEBROWSER SETTINGS
#-------------------------------------------------------------------------------
FILEBROWSER_URL_FILEBROWSER_MEDIA = STATIC_URL + "filebrowser/"
FILEBROWSER_PATH_FILEBROWSER_MEDIA = os.path.join(STATIC_URL, 'filebrowser/')
FILEBROWSER_EXTENSIONS = {
    'Folder': [''],
    'Image': ['.jpg','.jpeg','.gif','.png','.tif','.tiff'],
    'Video': ['.mov','.wmv','.mpeg','.mpg','.avi','.rm','.swf'],
    'Document': ['.pdf','.doc','.rtf','.txt','.xls','.csv'],
    'Sound': ['.mp3','.mp4','.wav','.aiff','.midi','.m4p'],
    'Code': ['.html','.py','.js','.css'],
}
FILEBROWSER_ADMIN_THUMBNAIL = 'fb_thumb'
FILEBROWSER_IMAGE_MAXBLOCK = 1024*1024
FILEBROWSER_MAX_UPLOAD_SIZE = 10485760 # 10485760 bytes = about 10megs
FILEBROWSER_VERSIONS = {
    'fb_thumb': {'verbose_name': 'Admin Thumbnail', 'width': 60, 'height': 60, 'opts': 'crop upscale'},
    'thumb': {'verbose_name': 'Grid Thumb', 'width': 150, 'height': 150, 'opts': 'crop upscale'},
    'small': {'verbose_name': 'Small (210px)', 'width': 210, 'height': '', 'opts': ''},
    'medium': {'verbose_name': 'Medium (370px)', 'width': 370, 'height': '', 'opts': ''},
    'large': {'verbose_name': 'Large (530px)', 'width': 530, 'height': '', 'opts': ''},
}
FILEBROWSER_ADMIN_VERSIONS = [
    'thumb', 'small', 'medium', 'large',
]


#-------------------------------------------------------------------------------
#	STORAGES SETTINGS
#-------------------------------------------------------------------------------
DEFAULT_FILE_STORAGE = 'apps.alltoez.storage.MediaFilesStorage'

#-------------------------------------------------------------------------------
#	CELERY SETTINGS
#-------------------------------------------------------------------------------
try:
    redis_url = urlparse.urlparse(os.environ.get('REDISCLOUD_URL'))
    BROKER_URL = 'redis://:%s@%s:%s/0' % (redis_url.password, redis_url.hostname, redis_url.port)
except:
    BROKER_URL = 'sqs://'
CELERY_RESULT_BACKEND = BROKER_URL
CELERY_SEND_TASK_ERROR_EMAILS = True
CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER = 'json'

CELERYBEAT_SCHEDULE = {
    'parse-events-everyday': {
        'task': 'apps.events.tasks.scrape_events_look_ahead',
        'schedule': timedelta(days=1),
    },
    'parse-venues-everyday': {
        'task': 'apps.venues.tasks.check_invalid_venues',
        'schedule': timedelta(days=2),
    },
}


CELERY_TASK_PUBLISH_RETRY_POLICY = {
    'max_retries': 15,
    'interval_start': 1,
    'interval_step': 10,
    'interval_max': 3600,
}


#-------------------------------------------------------------------------------
#	ADMIN SHORTCUT SETTINGS
#-------------------------------------------------------------------------------
ADMIN_SHORTCUTS = [
    {
        'shortcuts': [
            {
                'url': '/',
                'open_new_window': True,
            },
            {
                'url': '/admin/events/event/?end_date=unexpired',
                'title': 'Unexpired events',
            },
            {
                'url': '/admin/filebrowser/browse/',
                'title': 'Files',
                'class': 'folder'
            },
            {
                'url_name': 'admin:auth_user_changelist',
                'title': 'Users',
            },
        ]
    },
]
ADMIN_SHORTCUTS_SETTINGS = {
    'hide_app_list': False,
    'open_new_window': False,
}

#-------------------------------------------------------------------------------
#	MARKDOWN_DEUX CONFIG
#-------------------------------------------------------------------------------
MARKDOWN_DEUX_STYLES = {
    "default": {
        "extras": {
            "tables": None,
        },
        "safe_mode": False,
    },
}

#-------------------------------------------------------------------------------
#	GEOIP CONFIG
#-------------------------------------------------------------------------------
GEOIP_PATH = os.path.join(SITE_ROOT, "data/geoip_data")

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

#-------------------------------------------------------------------------------
#	HAYSTACK CONFIG
#-------------------------------------------------------------------------------
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
if 'BONSAI_URL' in os.environ:
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
            'URL': os.environ.get('BONSAI_URL'),
            'INDEX_NAME': 'haystack',
            'INCLUDE_SPELLING': True,
        },
    }

#-------------------------------------------------------------------------------
#	CREDENTIALS CONFIG
#-------------------------------------------------------------------------------
GOOGLE_ANALYTICS_CODE = os.environ.get('GOOGLE_ANALYTICS_CODE', None)
FACEBOOK_APP_ID = os.environ.get('FACEBOOK_APP_ID', "")
FLICKR_API_KEY = os.environ.get('FLICKR_API_KEY', "")
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY', "")
GOOGLE_SENGINE_ID = os.environ.get('GOOGLE_SENGINE_ID', "")
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', "")
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', "")
GOOGLE_MAPS_V3_APIKEY = os.environ.get('GOOGLE_MAPS_V3_APIKEY', "")
MANDRILL_API_KEY = os.environ.get('MANDRILL_APIKEY', "")

#-------------------------------------------------------------------------------
#	PREDICTIONIO CONFIG
#-------------------------------------------------------------------------------
PIO_ACCESS_KEY = os.environ.get('PIO_ACCESS_KEY', "")
PIO_ENGINE_ENDPOINT = os.environ.get('PIO_ENGINE_ENDPOINT', "")
PIO_EVENT_SERVER_ENDPOINT = os.environ.get('PIO_EVENT_SERVER_ENDPOINT', "")

#-------------------------------------------------------------------------------
#	LOGGING
#-------------------------------------------------------------------------------
from sorl.thumbnail.log import ThumbnailLogHandler
handler = ThumbnailLogHandler()
handler.setLevel(logging.ERROR)
logging.getLogger('sorl.thumbnail').addHandler(handler)

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
        'django': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}

try:
    from local_settings import *
except ImportError:
    pass

# Add the debug info apps after local settings has been imported
USE_DEBUG_TOOLBAR = False
if DEBUG and USE_DEBUG_TOOLBAR:
    TEMPLATE_CONTEXT_PROCESSORS += ('django.core.context_processors.debug',)
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    INSTALLED_APPS += ('haystack_panel', 'debug_toolbar',)
    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
        'haystack_panel.panel.HaystackDebugPanel'
    ]