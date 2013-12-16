
#
# Zink
#

from django.shortcuts import render

from util.generic import get_static
from util.deployment import get_deployment

from blog.models import Entry

import logging
logger = logging.getLogger("elevenbits")


def home(request):
    """Show the home page."""

    static = get_static("home.header")
    deployment = get_deployment()

    entry_list = Entry.objects.filter(active=True).reverse()
    logger.info("Retrieved %s blog entries." % len(entry_list))

    attributes = {'deployment': deployment,
                  'entries': entry_list,
                  'static': static}

    return render(request, 'index.html', attributes)
