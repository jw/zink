from django.shortcuts import render

from util.generic import get_static
from util.deployment import get_deployment

from haystack.forms import SearchForm


def search(request):
    """The search page."""
    form = SearchForm(request.GET)
    static = get_static("search.header")
    deployment = get_deployment()
    entries = form.search()

    attributes = {'deployment': deployment,
                  'static': static,
                  'entries': entries}

    return render(request, 'search.html', attributes)
