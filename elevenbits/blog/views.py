from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.conf import settings

from elevenbits.blog.models import Entry
from elevenbits.blog.models import Tag
from elevenbits.static.models import Static
from elevenbits.deployment.models import Deployment 

import logging

# let latest deployment
def get_deployment():
    deployment = {}
    last = Deployment.objects.all().reverse()[0]
    # TODO: handle 
    deployment['tag'] = last.tag
    deployment['timestamp'] = last.timestamp
    deployment['version'] = last.version
    deployment['deployer'] = last.deployer
    return deployment

def get_static():
    static = {}
    static['copyright'] = Static.objects.get(name="copyright").value
    return static

def index(request, page=1):

    deployment = get_deployment()
    
    static = get_static()
    static['title'] = Static.objects.get(name="index.title").value
    static['header'] = Static.objects.get(name="index.header").value
    
    entry_list = Entry.objects.filter(active=True).reverse()
    
    try:
        size = settings.BLOG_PAGE_SIZE
    except AttributeError:
        size = 5
    paginator = Paginator(entry_list, size)
    
    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(page)
    except ValueError:
        page = 1

    # If page is out of range, deliver last page.
    try:
        entries = paginator.page(page)
    except (EmptyPage, InvalidPage):
        entries = paginator.page(paginator.num_pages)

    attributes = {'deployment': deployment,
                  'static': static,
                  'entries': entries}

    # the context_instance will make sure that the default
    # TEMPLATE_CONTEXT_PROCESSORS are executed, among which
    # the django.core.context_processors.media.  That way
    # the MEDIA_URL will become part of the session.
    return render_to_response('index.html', 
                              attributes,
                              context_instance=RequestContext(request))

def detail(request, id):
    
    deployment = get_deployment()
    
    static = get_static()
    static['title'] = Static.objects.get(name="index.title").value
    static['header'] = Static.objects.get(name="index.header").value
    
    entry = get_object_or_404(Entry, pk=id)

    return render_to_response('detail.html', 
                              {'deployment': deployment,
                               'static': static,
                               'entry': entry},
                               context_instance=RequestContext(request))
    
def tags(request, tag, page=1):
    
    deployment = get_deployment()

    static = get_static()
    static['title'] = Static.objects.get(name="tags.title").value
    
    entry_list = Entry.objects.filter(tags__pk=tag).reverse()
    
    # create the header
    try:
        tag = Tag.objects.get(id=tag)
        static['header'] = str(entry_list.count()) + " entries tagged with '" + tag.tag + "'"
    except Tag.DoesNotExist:
        static['header'] = "Tag with id " + tag + " not found."

    try:
        size = settings.BLOG_PAGE_SIZE
    except AttributeError:
        size = 5
    paginator = Paginator(entry_list, size)
    
    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(page)
    except ValueError:
        page = 1

    # If page is out of range, deliver last page.
    try:
        entries = paginator.page(page)
    except (EmptyPage, InvalidPage):
        entries = paginator.page(paginator.num_pages)

    attributes = {'deployment': deployment,
                  'static': static,
                  'id': tag.id,
                  'entries': entries}

    return render_to_response('tagged.html', 
                              attributes,
                              context_instance=RequestContext(request))

