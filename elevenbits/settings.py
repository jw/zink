
#
# Copyright (c) 2013-2016 Jan Willems (ElevenBits)
#
# This file is part of Zink.
#
# Zink is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Zink is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Zink.  If not, see <http://www.gnu.org/licenses/>.
#

#
# public settings for all sites handled by this Django instance, i.e.
# [www.]elevenbits.org, [www.]elevenbits.com, vonk.elevenbits.org and m8n.be
#

from os.path import join, dirname, realpath
from socket import gethostname

SITE_ROOT = dirname(realpath(join(__file__, "..")))

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1",
                 "localhost",
                 ".elevenbits.com",
                 ".elevenbits.org",
                 ".elevenbits.be",
                 ".m8n.be"]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'zink',
        'USER': 'postgres',
        'PASSWORD': 'P4t3rsB3rg',
        'HOST': 'localhost',
        'DATABASE_PORT': '',
    }
}


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

SITE_ID = 1

# use i18n l10n and make dates time zone
USE_I18N = True
USE_L10N = True
USE_TZ = False

# The statics (css and images) location
STATICFILES_DIRS = (
    join(SITE_ROOT, "assets"),
)

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder"
)

STATIC_ROOT = '/var/www/assets/zink/'
STATIC_URL = 'https://assets.elevenbits.com/'

FIXTURE_DIRS = (join(SITE_ROOT, 'fixtures'),)

# TODO: read up on this
# CONTEXT_PREPROCESSORS = (
#    "django.contrib.auth.context_processors.auth",
#    "django.core.context_processors.debug",
#    "django.core.context_processors.i18n",
#    "django.core.context_processors.media",
#    "django.core.context_processors.static",
#    "django.core.context_processors.tz",
#    "django.contrib.messages.context_processors.messages",
# )


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            join(dirname(__file__), 'templates').replace('\\', '/')
        ],
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
                # needed for current menu identifier:
                'django.template.context_processors.request'
            ],
        },
    },
]

MIDDLEWARE_CLASSES = (
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'tracking.middleware.BannedIPMiddleware',
    # 'tracking.middleware.VisitorTrackingMiddleware',
    # 'tracking.middleware.VisitorCleanUpMiddleware',
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
    'django_extensions',
    # django contribs
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'haystack',
    # zink apps
    #'elevenbits.menu_extras',  # TODO: move this in apps root
    'blog.apps.BlogConfig',
    'static.apps.StaticConfig',
    'contact',
    'home',
    'deployment.apps.DeploymentConfig',
    'elevenbits',
    #'search',
    #'treemenus',  # TODO: make sure to use the proper (Russian) one!
    # utilities
    # 'tracking',
    'util',
    # 'django_crontab',
    #'tweeter',
    # 'debug_toolbar',
)

#
# ElevenBits constants
#

BLOG_PAGE_SIZE = 4
CLIENT_LOGO_MARGIN = 20

#
# TODO: update the logging part
#

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
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
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO'
        },
    },
}

# hostname based settings
hostname = gethostname()
if "elevenbits" in hostname:
    from .settings_elevenbits import *
elif "m8n" in hostname:
    from .settings_m8n import *
else:
    # localhost will enable DEBUG
    from .settings_localhost import *

# FIXME
SECRET_KEY=12345098563248723469823