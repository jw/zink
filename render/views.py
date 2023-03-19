import logging

from django.shortcuts import render

from blog.models import Entry

logger = logging.getLogger("zink")


def index(request):  # noqa: ANN001
    entry_list = Entry.objects.filter(page=Entry.BLOG, active=True).reverse()
    logger.warning(f"Retrieved {len(entry_list)} blog entries.")

    attributes = {
        "entry": entry_list[0],
    }

    return render(request, "index.html", attributes)


def about(request):
    logger.warning("About!")
    return render(request, "about.html", {})


def cookies(request):
    logger.warning("Cookies!")
    return render(request, "cookies.html", {})
