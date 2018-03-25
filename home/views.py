
import logging

from django.shortcuts import render

from blog.models import Entry
from elevenbits.generic import get_assets
from reading.models import Text
from util.deployment import get_deployment

logger = logging.getLogger("elevenbits")


def home(request):
    """Show the home page."""

    assets = get_assets("index.header")
    deployment = get_deployment()

    entry_list = Entry.objects.filter(active=True).reverse()
    logger.info(f"Retrieved {len(entry_list)} blog entries.")

    book = Text.objects.filter(reading=True).first()
    logger.info(f"Found a book: {book}.")

    try:
        entry = entry_list.first()
    except IndexError:
        entry = None

    attributes = {'deployment': deployment,
                  'entry': entry,
                  'entries': entry_list[1:],
                  'book': book,
                  'assets': assets}

    return render(request, 'index.html', attributes)
