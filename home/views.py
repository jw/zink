
#
# Zink
#

from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.mail import send_mail

from elevenbits.static.models import Static
from elevenbits.deployment.models import Deployment

from contact.models import Contact, ContactForm

import logging
logger = logging.getLogger("elevenbits")


# TODO: generalize this!
def get_deployment():
    """Get latest deployment."""
    deployment = {}
    try:
        last = Deployment.objects.all().reverse()[0]
        deployment['tag'] = last.tag
        deployment['timestamp'] = last.timestamp
        deployment['version'] = last.version
        deployment['deployer'] = last.deployer
    except IndexError:
        from datetime import datetime
        deployment['tag'] = "unknown"
        deployment['timestamp'] = datetime.now()
        deployment['version'] = "unknown"
        deployment['deployer'] = "unknown"
    return deployment


def home(request):
    """
    Show the home page.
    """

    #
    # Generate generic attributes, deployment and contact data
    #

    attributes = {}

    # TODO: make this: attributes['static'] = get_statics('contact')
    static = {}
    static['host'] = Static.objects.get(name="header.host").value
    static['description'] = Static.objects.get(name="header.description").value
    static['title'] = Static.objects.get(name="home.title").value
    attributes['static'] = static

    attributes['deployment'] = get_deployment()

    return render(request, 'index.html', attributes)
