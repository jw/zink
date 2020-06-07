import os
from pathlib import Path

import dj_database_url
from environs import Env
from os.path import join, dirname, abspath
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

env = Env()
env.read_env()
root = Path(__file__).parents[1]
SITE_ROOT = str(root)
PORT = os.environ.get('PORT', 8000)
DEBUG = env.bool('DEBUG', False)

print(f"DATABASE_URL={os.environ.get('DATABASE_URL')}")
print(f"DEBUG={DEBUG}")
print(f"PORT={PORT}")

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

# email
EMAIL_HOST = env('MAILGUN_HOST')
EMAIL_PORT = os.environ['MAILGUN_PORT']
EMAIL_HOST_USER = os.environ['MAILGUN_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['MAILGUN_HOST_PASSWORD']
EMAIL_USE_TLS = True
EMAIL_BASE = os.environ['MAILGUN_BASE_URL']

GOOGLE_MAPS_KEY = os.environ['GOOGLE_MAPS_KEY']

DATABASES = {
    'default': env.dj_db_url('DATABASE_URL'),
}

db_from_env = dj_database_url.config()
# print(f"DB env: {db_from_env}")
DATABASES['default'].update(db_from_env)

#
# Test properties
#

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

try:
    import rainbowtests  # noqa

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
USE_TZ = True

# The statics (css and images) location
STATICFILES_DIRS = (
    join(SITE_ROOT, "assets"),
    # join(SITE_ROOT, "tmp"),
)

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    # 'static_precompiler.finders.StaticPrecompilerFinder',
    "compressor.finders.CompressorFinder",
)

# compressor
COMPRESS_ENABLED = True
print(os.environ['COMPRESS_OFFLINE'])
if not os.environ['COMPRESS_OFFLINE']:
    print(f"IN HEROKU, so not running compress, since we are in OFFLINE mode: {os.environ['COMPRESS_OFFLINE']}.")
    COMPRESS_OFFLINE = True
else:
    print("LOCAL (not in Heroku land), so compress is ONLINE.")
COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)
COMPRESS_ROOT = join(SITE_ROOT, "elevenbits", "theme")

PROJECT_ROOT = abspath(dirname(__file__))

STATIC_ROOT = join(PROJECT_ROOT, 'assets/')
STATIC_URL = '/assets/'

MEDIA_URL = '/media/'
MEDIA_ROOT = join(PROJECT_ROOT, 'media')

# STATICFILES_STORAGE = 'whitenoise.storage.' \
#                       'CompressedManifestStaticFilesStorage'
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
            ],
        },
    },
]

MIDDLEWARE = (
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'tracking.middleware.BannedIPMiddleware',
    # 'tracking.middleware.VisitorTrackingMiddleware',
    # 'tracking.middleware.VisitorCleanUpMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.gzip.GZipMiddleware',
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
    'widget_tweaks',
    'django_extensions',
    # django contribs
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.messages',

    # css
    "compressor",

    # statics
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',

    'haystack',

    # 'static_precompiler',
    'blog.apps.BlogConfig',
    'contact',
    'deployment.apps.DeploymentConfig',
    'elevenbits',
    # 'search',
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

sentry_sdk.init(
    dsn="https://" + env('SENTRY_PUBLIC_KEY') + ':' +
        env('SENTRY_SECRET_KEY') + "@sentry.io/" +
        env('SENTRY_PROJECT'),
    integrations=[DjangoIntegration()],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['console'],  # sentry
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
        # 'sentry': {
        #     'level': 'WARNING',
        #     'class': 'raven.contrib.django.raven_compat.'
        #              'handlers.SentryHandler',
        #     'tags': {'custom-tag': 'x'},
        # },
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
        # 'raven': {
        #     'level': 'DEBUG',
        #     'handlers': ['console'],
        #     'propagate': False,
        # },
        # 'sentry.errors': {
        #     'level': 'DEBUG',
        #     'handlers': ['console'],
        #     'propagate': False,
        # },
    },
}
