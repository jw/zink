import logging
from pathlib import Path

from django.shortcuts import render

from zink import settings

log = logging.getLogger(__name__)


def stilus(request):

    p = Path(settings.BASE_DIR)
    dir = p.glob('**')

    print(f'dir: {list(dir)}')

    attributes = {'stilus': "Stilus!",
                  'debug': settings.DEBUG,
                  'dir': dir}

    return render(request, 'stilus.html', attributes)
