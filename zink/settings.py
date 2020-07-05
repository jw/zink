import os
import logging.config
from django.utils.log import DEFAULT_LOGGING

from environs import Env

logger = logging.getLogger('zink')

env = Env()
env.read_env()

# Disable Django's logging setup
LOGGING_CONFIG = None

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# get the environment variables from .env

# note: By default a non debug system at port 8000 without any
#       database and an open allowed host list will be set up.
#       The logging level of this system will be warning.

SECRET_KEY = env("DJANGO_SECRET_KEY", "some_invalid_secret_key")
PORT = env.int('PORT', 8000)
DEBUG = env.bool('DEBUG', False)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", ['*'])
HAS_DB_URL = env.str("DATABASE_URL", None)
LOGLEVEL = env.str('LOGLEVEL', 'WARNING').upper()

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            # exact format is not important, this is the minimum information
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
        'django.server': DEFAULT_LOGGING['formatters']['django.server'],
    },
    'handlers': {
        # console logs to stderr
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
        # Add Handler for Sentry for `warning` and above
        # 'sentry': {
        #     'level': 'WARNING',
        #     'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        # },
        'django.server': DEFAULT_LOGGING['handlers']['django.server'],
    },
    'loggers': {
        # default for all undefined Python modules
        '': {
            'level': 'WARNING',
            'handlers': ['console'],  # , 'sentry'],
        },
        # Our application code
        'zink': {
            'level': LOGLEVEL,
            'handlers': ['console'],  # , 'sentry'],
            # Avoid double logging because of root logger
            'propagate': False,
        },
        # Prevent noisy modules from logging to Sentry
        'noisy_module': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        # Default runserver request logging
        'django.server': DEFAULT_LOGGING['loggers']['django.server'],
    },
})

logger.info('ENVIRONMENT SETTINGS:')
if HAS_DB_URL:
    logger.info(f" > DATABASE_URL={HAS_DB_URL}")
else:
    logger.warning('No database url specified; '
                   'should be in docker build.')
logger.info(f" > DEBUG={DEBUG}")
logger.info(f" > PORT={PORT}")
logger.info(f" > BASE_DIR={BASE_DIR}")
logger.info(f" > LOGLEVEL={LOGLEVEL}")

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'zink',
    'blog',
    'compressor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'zink.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'zink.wsgi.application'

if HAS_DB_URL:
    DATABASES = {"default": env.dj_db_url("DATABASE_URL")}
    logger.info(f' > DATABASES={DATABASES}')

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)
logger.info(f" > STATIC_URL={STATIC_URL}")
logger.info(f" > STATIC_ROOT={STATIC_ROOT}")

COMPRESS_OFFLINE = True
COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)

logger.info('')  # cleanup
