import os
from os.path import join, dirname, abspath
from pathlib import Path

import dj_database_url
import sentry_sdk
from environs import Env
from sentry_sdk.integrations.django import DjangoIntegration

env = Env()
env.read_env()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PORT = os.environ.get('PORT', 8000)
DEBUG = env.bool('DEBUG', False)

print(f"DATABASE_URL={env('DATABASE_URL')}")
print(f"DEBUG={DEBUG}")
print(f"PORT={env('PORT')}")
print(f"BASE_DIR={BASE_DIR}")

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
# EMAIL_HOST = env('MAILGUN_HOST')
# EMAIL_PORT = os.environ['MAILGUN_PORT']
# EMAIL_HOST_USER = os.environ['MAILGUN_HOST_USER']
# EMAIL_HOST_PASSWORD = os.environ['MAILGUN_HOST_PASSWORD']
# EMAIL_USE_TLS = True
# EMAIL_BASE = os.environ['MAILGUN_BASE_URL']

# GOOGLE_MAPS_KEY = os.environ['GOOGLE_MAPS_KEY']

DATABASES = {"default": env.dj_db_url("DATABASE_URL")}
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }
#
# DATABASE_URL = os.environ.get('DATABASE_URL')
# db_from_env = dj_database_url.config(default=DATABASE_URL, conn_max_age=500, ssl_require=True)
# DATABASES['default'].update(db_from_env)

# DATABASES = {
#     'default': env.dj_db_url('DATABASE_URL'),
# }

print(f'DATABASE_URL: {env("DATABASE_URL")}')
print(f'DATABASES: {DATABASES}')

# db_from_env = dj_database_url.config()
# print(f"DB env: {db_from_env}")
# DATABASES['default'].update(db_from_env)

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

SECRET_KEY = env('SECRET_KEY', 'invalid_secret_key')

SITE_ID = 1

# use i18n l10n and make dates time zone
USE_I18N = True
USE_L10N = True
USE_TZ = True

# statics and compress

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)

COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)

COMPRESS_OFFLINE = 'Hello'

MEDIA_URL = '/media/'
MEDIA_ROOT = join(BASE_DIR, 'media')

FIXTURE_DIRS = (join(BASE_DIR, 'fixtures'),)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        # 'DIRS': [join(BASE_DIR, 'uploads/templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                # 'django.template.context_processors.i18n',
                # 'django.template.context_processors.media',
                # 'django.template.context_processors.static',
                # 'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

MIDDLEWARE = (
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'tracking.middleware.BannedIPMiddleware',
    # 'tracking.middleware.VisitorTrackingMiddleware',
    # 'tracking.middleware.VisitorCleanUpMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.middleware.gzip.GZipMiddleware',
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
    # 'widget_tweaks',
    # 'django_extensions',
    # django contribs
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    "compressor",

    # 'haystack',

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
