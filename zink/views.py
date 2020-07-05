import logging

from django.shortcuts import render

log = logging.getLogger(__name__)


def stilus(request):

    attributes = {'stilus': "Stilus!",}

    return render(request, 'stilus.html', attributes)
