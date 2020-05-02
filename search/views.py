from bs4 import BeautifulSoup
from django.forms import Form
from django.shortcuts import render
from haystack.generic_views import SearchView

from elevenbits.generic import get_assets
from util.deployment import get_deployment


def remove_tags(text):
    soup = BeautifulSoup(text)
    return soup.get_text()


class MySearchView(SearchView):
    """My custom search view."""

    def get_queryset(self):
        queryset = super(MySearchView, self).get_queryset()
        # further filter queryset based on some set of criteria
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(MySearchView, self).get_context_data(*args, **kwargs)
        # do something
        return context


def search(request):
    """The search page."""

    form = Form(request.GET, load_all=True)
    # entries = form.search()
    tags = []
    blogs = []
    # for entry in entries:
    #     if entry.model_name == 'tag':
    #         tags.append(entry)
    #     elif entry.model_name == 'entry' and entry.object.active:
    #         blogs.append(entry)
    #
    query = form.data['q']
    #
    static = get_assets("blog.header")
    deployment = get_deployment()

    attributes = {'deployment': deployment,
                  'assets': static,
                  'blogs': blogs,
                  'tags': tags,
                  'query': query}

    return render(request, 'search.html', attributes)
