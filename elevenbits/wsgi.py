import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "elevenbits.settings")

# This application object should only be used by the development server.
# The staging and production servers should use uwsgi!
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
