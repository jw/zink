from os.path import join, dirname, realpath, abspath
from socket import gethostname

import dj_database_url
import environ

root = environ.Path(__file__) - 2
env = environ.Env()
environ.Env.read_env()

SITE_ROOT = root()

DEBUG = env.bool('DEBUG', False)

# TODO: use .env for this
ALLOWED_HOSTS = ["127.0.0.1",
                 "localhost",
                 "elevenbits-zink.herokuapp.com",
                 "elevenbits-zink.herokudns.com",
                 ".elevenbits.com.herokudns.com",
                 ".elevenbits.com",
                 ".elevenbits.org",
                 ".elevenbits.be",
                 ".m8n.be"]

EMAIL_HOST = env('MAILGUN_HOST')
EMAIL_PORT = env('MAILGUN_PORT')
EMAIL_HOST_USER = env('MAILGUN_HOST_USER')
EMAIL_HOST_PASSWORD = env('MAILGUN_HOST_USER')
EMAIL_USE_TLS = True
EMAIL_BASE = env('MAILGUN_BASE_URL')

GOOGLE_MAPS_KEY = env('GOOGLE_MAPS_KEY')

DATABASES = {
    'default': env.db('DATABASE_URL'),
}

db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)

#
# Test properties
#

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

try:
    import rainbowtests

    TEST_RUNNER = 'rainbowtests.RainbowTestSuiteRunner'
except ImportError:
    pass

#
# Debug toolbar
#

INTERNAL_IPS = ('127.0.0.1',)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

# Note:
# never add 'debug_toolbar.middleware.DebugToolbarMiddleware' to
# the debug panel!
# DEBUG_TOOLBAR_PANELS = (
#     'debug_toolbar.panels.version.VersionDebugPanel',
#     'debug_toolbar.panels.timer.TimerDebugPanel',
#     'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
#     'debug_toolbar.panels.headers.HeaderDebugPanel',
#     'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
#     'debug_toolbar.panels.sql.SQLDebugPanel',
#     'debug_toolbar.panels.template.TemplateDebugPanel',
#     'debug_toolbar.panels.cache.CacheDebugPanel',
#     'debug_toolbar.panels.signals.SignalDebugPanel',
#     'debug_toolbar.panels.logger.LoggingPanel',
# )

#
# Administrators
#

ADMINS = (
    ('Jan Willems', 'jw@elevenbits.com'),
)
MANAGERS = ADMINS

TIME_ZONE = 'Europe/Brussels'
LANGUAGE_CODE = 'en-BE'

SECRET_KEY = env('SECRET_KEY')

SITE_ID = 1

# use i18n l10n and make dates time zone
USE_I18N = True
USE_L10N = True
USE_TZ = False

# The statics (css and images) location
STATICFILES_DIRS = (
    join(SITE_ROOT, "assets"),
    join(SITE_ROOT, "tmp"),
)

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    # 'static_precompiler.finders.StaticPrecompilerFinder',
)

STATIC_PRECOMPILER_COMPILERS = (
    ('static_precompiler.compilers.Stylus',
     {"executable": "/home/jw/.nvm/versions/node/v6.11.2/bin/stylus",
      "sourcemap_enabled": True}),
)

PROJECT_ROOT = abspath(dirname(__file__))

STATIC_ROOT = join(PROJECT_ROOT, 'staticfiles/')
STATIC_URL = '/assets/'

MEDIA_URL = '/media/'
MEDIA_ROOT = join(PROJECT_ROOT, 'media')

# STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# SECURE_HSTS_SECONDS = 60
# SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
#     'DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True)
# SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
#     'DJANGO_SECURE_CONTENT_TYPE_NOSNIFF', default=True)
# SECURE_BROWSER_XSS_FILTER = True
# SESSION_COOKIE_SECURE = True
# SESSION_COOKIE_HTTPONLY = True
# SECURE_SSL_REDIRECT = env.bool('DJANGO_SECURE_SSL_REDIRECT', default=True)
# CSRF_COOKIE_SECURE = True
# CSRF_COOKIE_HTTPONLY = True
# X_FRAME_OPTIONS = 'DENY'


PIPELINE = {
    'STYLESHEETS': {
        'colors': {
            'source_filenames': (
                # 'css/core.css',
                # 'css/colors/*.css',
                # 'css/layers.css'
            ),
            'output_filename': 'css/colors.css',
            'extra_context': {
                'media': 'screen, projection',
            },
        },
    },
    'JAVASCRIPT': {
        'stats': {
            'source_filenames': (
                # 'js/jquery.js',
                # 'js/d3.js',
                # 'js/collections/*.js',
                # 'js/application.js',
            ),
            'output_filename': 'js/stats.js',
        }
    }
}

FIXTURE_DIRS = (join(SITE_ROOT, 'fixtures'),)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [join(PROJECT_ROOT, 'uploads/templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                # needed for current menu identifier (for sitetree):
                'django.template.context_processors.request'
            ],
        },
    },
]

MIDDLEWARE = (
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'tracking.middleware.BannedIPMiddleware',
    # 'tracking.middleware.VisitorTrackingMiddleware',
    # 'tracking.middleware.VisitorCleanUpMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
)

ROOT_URLCONF = 'elevenbits.urls'

WSGI_APPLICATION = 'elevenbits.wsgi.application'

# CRONJOBS = [
#     ('*/5 * * * *', 'tweeter.admin.get_latest_tweets'),
# ]

# tweeter.admin

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': join(dirname(__file__), 'whoosh_index'),
    },
}

INSTALLED_APPS = (
    'raven.contrib.django.raven_compat',
    'widget_tweaks',
    'django_extensions',
    # django contribs
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'static_precompiler',
    'blog.apps.BlogConfig',
    'static.apps.StaticConfig',
    'contact',
    'home',
    'deployment.apps.DeploymentConfig',
    'elevenbits',
    # 'search',
    'sitetree',
    'reading',
    'util',
    # 'django_crontab',
    # 'tweeter',
    # 'debug_toolbar',
    # 'menu'
)

#
# ElevenBits constants
#

BLOG_PAGE_SIZE = 4
CLIENT_LOGO_MARGIN = 20

RAVEN_CONFIG = {
    'dsn': 'https://' + env('SENTRY_PUBLIC_KEY') + ':' +
           env('SENTRY_SECRET_KEY') + '@sentry.io/' +
           env('SENTRY_PROJECT')
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['console', 'sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s ' +
                      '%(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
    },
    'handlers': {
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO'
        },
        'elevenbits': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False
        },
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}
