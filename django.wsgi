import os
import sys

sys.path.append('/home/jw/python/workspace/elevenbits')

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
