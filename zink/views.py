import logging

from django.shortcuts import render

from zink import settings

log = logging.getLogger(__name__)


def stilus(request):

    attributes = {'stilus': "Stilus!",
                  'debug': settings.DEBUG}

    return render(request, 'stilus.html', attributes)
