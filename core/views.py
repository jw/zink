import logging

from django.shortcuts import render

from blog.models import Entry

logger = logging.getLogger("zink")


def index(request):  # noqa: ANN001
    latest_entry = (
        Entry.objects.filter(page=Entry.BLOG, active=True).order_by("-posted").first()
    )
    logger.warning(f"Retrieved latest blog entry: {latest_entry}.")

    attributes = {
        "latest_entry": latest_entry,
    }

    return render(request, "index.html", attributes)


def about(request):
    logger.warning("About!")
    return render(request, "about.html", {})


def cookies(request):
    logger.warning("Cookies!")
    return render(request, "cookies.html", {})


def projects(request):
    logger.warning("Projects!")
    return render(request, "projects.html", {})


def contact(request):
    logger.warning("Contact!")
    return render(request, "contact.html", {})
