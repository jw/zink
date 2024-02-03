import logging

from django.shortcuts import render

from blog.models import Entry

logger = logging.getLogger("zink")


def index(request):  # noqa: ANN001
    entries = Entry.objects.filter(page=Entry.BLOG, active=True).reverse()
    logger.warning(f"Retrieved {len(entries)} blog entries.")

    attributes = {
        "entries": entries,
    }

    return render(request, "index.html", attributes)


def about(request):
    logger.warning("About!")
    return render(request, "about.html", {})


def cookies(request):
    logger.warning("Cookies!")
    return render(request, "cookies.html", {})
