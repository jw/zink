import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

SECRET_ENV = Path("/") / "etc" / "secret" / ".env"
if SECRET_ENV.exists():
    load_dotenv(SECRET_ENV)
else:
    load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ["SECRET_KEY"]

DEBUG = bool(os.environ.get("DEBUG", False))
RENDER = os.environ.get("RENDER", False)

ALLOWED_HOSTS = []
CSRF_TRUSTED_ORIGINS = []

RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

ALLOWED_HOST = os.environ.get("ALLOWED_HOST")
if ALLOWED_HOST:
    ALLOWED_HOSTS.append(ALLOWED_HOST)
    CSRF_TRUSTED_ORIGINS.append(f"https://{ALLOWED_HOST[1:]}")

print(f"{ALLOWED_HOST=}")
print(f"{CSRF_TRUSTED_ORIGINS=}")

INSTALLED_APPS = [
    "core.apps.CoreConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "blog",
    "deployment",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "elevenbits.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "elevenbits.wsgi.application"

default_database = dj_database_url.config(
    default=(
        f"postgresql://{os.getenv('POSTGRES_USER', default='zink')}:"
        f"{os.getenv('POSTGRES_PASSWORD', default='zink')}@"
        f"{os.getenv('POSTGRES_HOST', default='localhost')}:"
        f"{os.getenv('POSTGRES_PORT', default=5432)}/"
        f"{os.getenv('POSTGRES_DB', default='zink')}"
    ),
    conn_max_age=600,
)
DATABASES = {"default": default_database}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

if RENDER:
    # Tell Django to copy statics to the `staticfiles` directory
    # in your application directory on Render.
    STATIC_ROOT = BASE_DIR / "staticfiles"

    # Turn on WhiteNoise storage backend that takes care of compressing static files
    # and creating unique names for each version so they can safely be cached forever.
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
