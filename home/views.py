import logging

from django.shortcuts import render

from blog.models import Entry, Menu
from blog.views import create_menus
from elevenbits.generic import get_assets
from reading.models import Text

logger = logging.getLogger("elevenbits")


def home(request):
    """Show the home page."""

    assets = get_assets(prefix="index")

    menus = create_menus(Menu.roots[0])
    logger.info(f"Retrieved {len(menus)} menu items.")

    entry_list = Entry.objects.filter(active=True).reverse()
    logger.info(f"Retrieved {len(entry_list)} blog entries.")

    books = list(Text.objects.filter(reading=True))
    if books:
        logger.info(f"Reading one (or more) books: {books}.")
    else:
        logger.info("Not reading any book! So sad.")

    try:
        entry = entry_list.first()
    except IndexError:
        entry = None

    attributes = {'entry': entry,
                  'entries': entry_list[1:],
                  'books': books,
                  'menus': menus,
                  'assets': assets}

    return render(request, 'index.html', attributes)
