import logging
from os.path import join
from pathlib import Path

from django.shortcuts import render

from zink import settings

log = logging.getLogger(__name__)


def stilus(request):

    p = Path(settings.BASE_DIR)
    app_exists = p.exists()
    p = Path(settings.STATIC_ROOT)
    staticfiles_exists = p.exists()
    p = Path(join(settings.STATIC_ROOT, 'CACHE'))
    cache_exists = p.exists()

    p = Path(settings.STATIC_ROOT)
    dir = p.glob('**')

    print(f'dir: {list(dir)}')
    dir = p.glob('**')

    attributes = {'stilus': "Stilus!",
                  'debug': settings.DEBUG,
                  'app_exists': app_exists,
                  'staticfiles_exists': staticfiles_exists,
                  'cache_exists': cache_exists,
                  'dir': dir}

    return render(request, 'stilus.html', attributes)
