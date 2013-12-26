
#
# Zink
#

SECRET_KEY = '${project_key}'

#
# Database
#

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '${db_name}',
        'USER': '${db_username}',
        'PASSWORD': '${db_password}',
        'HOST': 'localhost',
        'DATABASE_PORT': '',
    }
}

#
# Email settings
#

EMAIL_HOST = '${email_host}'
EMAIL_PORT = ${email_port}
EMAIL_HOST_USER = '${email_user}'
EMAIL_HOST_PASSWORD = '${email_password}'
EMAIL_USE_TLS = ${email_tls}

#
# Twitter settings
#

TWITTER_NAME = "${twitter_name}"

CONSUMER_KEY = "${twitter_consumer_key}"
CONSUMER_SECRET = "${twitter_consumer_secret}"

OAUTH_TOKEN = "${twitter_oauth_token}"
OAUTH_TOKEN_SECRET = "${twitter_oauth_token_secret}"
