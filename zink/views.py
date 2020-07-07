import logging
from os.path import join
from pathlib import Path

from django.shortcuts import render

from blog.models import Menu, Entry
from blog.views import get_assets, create_menus
from zink import settings

logger = logging.getLogger(__name__)


def home(request):
    """Show the home page."""

    assets = get_assets(prefix="index")

    menus = create_menus(Menu.roots[0])
    logger.info(f"Retrieved {len(menus)} menu items.")

    entry_list = Entry.objects.filter(page=Entry.BLOG, active=True).reverse()
    logger.info(f"Retrieved {len(entry_list)} blog entries.")

    # books = list(Text.objects.filter(reading=True))
    # if books:
    #     logger.info(f"Reading one (or more) books: {books}.")
    # else:
    #     logger.info("Not reading any book! So sad.")

    try:
        entry = entry_list.first()
    except IndexError:
        entry = None

    attributes = {'entry': entry,
                  'entries': entry_list[1:],
                  # 'books': books,
                  'menus': menus,
                  'assets': assets}

    return render(request, 'index.html', attributes)


def stilus(request):

    logger.info('Stilus view called.')
    logger.warning('Stilus view called.')

    p = Path(settings.BASE_DIR)
    app_exists = p.exists()
    p = Path(settings.STATIC_ROOT)
    staticfiles_exists = p.exists()
    p = Path(join(settings.STATIC_ROOT, 'CACHE'))
    cache_exists = p.exists()

    p = Path(settings.STATIC_ROOT)
    dir = p.glob('**')

    attributes = {'stilus': "Stilus!",
                  'debug': settings.DEBUG,
                  'app_exists': app_exists,
                  'staticfiles_exists': staticfiles_exists,
                  'cache_exists': cache_exists,
                  'dir': dir}

    return render(request, 'stilus.html', attributes)
