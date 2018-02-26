from django.shortcuts import render

from util.generic import get_assets
from util.deployment import get_deployment

from bs4 import BeautifulSoup


def remove_tags(text):
    soup = BeautifulSoup(text)
    return soup.get_text()


def search(request):
    """The search page."""

    form = Form(request.GET, load_all=True)
    entries = form.search()
    tags = []
    blogs = []
    for entry in entries:
        if entry.model_name == 'tag':
            tags.append(entry)
        elif entry.model_name == 'entry' and entry.object.active:
            blogs.append(entry)

    query = form.data['q']

    static = get_assets("blog.header")
    deployment = get_deployment()

    attributes = {'deployment': deployment,
                  'assets': static,
                  'blogs': blogs,
                  'tags': tags,
                  'query': query}

    return render(request, 'search.html', attributes)
