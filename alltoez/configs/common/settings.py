import os, django, urllib
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
STATIC_ROOT = os.path.join(SITE_ROOT, "static")
MEDIA_ROOT = os.path.join(SITE_ROOT, "media")
STATIC_URL = "/static/"
MEDIA_URL = "/media/"

ADMINS = (('Devang Mundhra', 'devangmundhra@gmail.com'), ('Ruchika Damani', 'ruchikadamani90@gmail.com')),
MANAGERS = ADMINS

# Local time
TIME_ZONE = "UTC"
LANGUAGE_CODE = "en-us"
SITE_ID = 1
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
    os.path.join(SITE_ROOT, 'templates'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
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


#-------------------------------------------------------------------------------
#	APP SETTINGS
#-------------------------------------------------------------------------------
DEFAULT_PROFILE_IMAGE = os.path.join(MEDIA_ROOT, 'uploads/alltoez_defaults/profile_portrait_default.png')
GOOGLE_ANALYTICS_CODE = None
GOOGLE_MAPS_V3_APIKEY = "AIzaSyDOtkrcR4QFGYTMdR71WkkUYsMQ735c_EU"
LANGUAGES = (
    ('en', _('English')),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'alltoez',
        # 'USER': 'XXXXX',
        # 'PASSWORD': 'XXXX',
        'HOST': 'localhost',
    }
}
ROOT_URLCONF = 'alltoez.configs.common.urls'
AUTH_PROFILE_MODULE = 'alltoez_profile.UserProfile'

EMAIL_SUBJECT_PREFIX = "[Alltoez Server]"
SERVER_EMAIL = 'Alltoez Server <server@alltoez.com>'

#-------------------------------------------------------------------------------
#	CACHE SETTINGS
#-------------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'LOCATION': '127.0.0.1:11211',
        'KEY_PREFIX': 'alltoez:'
    }
}
CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 60
CACHE_MIDDLEWARE_KEY_PREFIX = 'alltoez:'

CACHEOPS_REDIS = {
    'host': 'localhost', # redis-server is on same machine
    'port': 6379,        # default redis port
    'db': 1,             # SELECT non-default redis database
                         # using separate redis db or redis instance
                         # is highly recommended
    'socket_timeout': 3,
}
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
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.yuglify.YuglifyCompressor'
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.yuglify.YuglifyCompressor'
PIPELINE_YUGLIFY_BINARY = os.path.join(SITE_ROOT, "../node_modules/yuglify/bin/yuglify")
PIPELINE_COFFEE_SCRIPT_BINARY = os.path.join(SITE_ROOT, "../node_modules/coffee-script/bin/coffee")
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
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

#-------------------------------------------------------------------------------
#	CELERY SETTINGS
#-------------------------------------------------------------------------------
BROKER_URL = 'redis://'
CELERY_RESULT_BACKEND = BROKER_URL
CELERY_SEND_TASK_ERROR_EMAILS = False
CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER = 'json'

CELERYBEAT_SCHEDULE = {
    'parse-events-everyday': {
        'task': 'apps.events.tasks.scrape_events_look_ahead',
        'schedule': timedelta(days=1),
    },
    'parse-venues-everyday': {
        'task': 'apps.venues.tasks.check_invalid_venues',
        'schedule': timedelta(days=20),
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