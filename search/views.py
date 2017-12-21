from django.shortcuts import render

from util.generic import get_static
from util.deployment import get_deployment

from bs4 import BeautifulSoup

from markdown.extensions import Extension
from markdown import markdown


class EscapeHtml(Extension):

    def extendMarkdown(self, md, md_globals):
        del md.preprocessors['html_block']
        del md.inlinePatterns['html']


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
            entry.object.plain = remove_tags(
                markdown(entry.object.body,
                         extensions=[EscapeHtml()]))
            blogs.append(entry)

    query = form.data['q']

    static = get_static("search.header")
    deployment = get_deployment()

    attributes = {'deployment': deployment,
                  'assets': static,
                  'blogs': blogs,
                  'tags': tags,
                  'query': query}

    return render(request, 'search.html', attributes)
