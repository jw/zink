from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from elevenbits.blog.models import Entry
from elevenbits.blog.models import Tag
from elevenbits.static.models import Static

from elevenbits.guest.decorators import guest_allowed, login_required

import logging

def get_static():
    static = {}
    static['deployment_time'] = Static.objects.get(name="deployment.time").value
    static['copyright'] = Static.objects.get(name="copyright").value
    return static

@guest_allowed
def index(request, page=0):
    static = get_static()
    static['title'] = Static.objects.get(name="index.title").value
    static['header'] = Static.objects.get(name="index.header").value
    logging.debug("There are " + str(Entry.objects.filter(active=True).count()) + " active log entries.")
    last_page = (Entry.objects.filter(active=True).count() - 1)/5
    logging.debug("position: 0 | " + str(page) + " | " + str(last_page))
    latest_entry_list = Entry.objects.filter(active=True).reverse()[int(page)*5:int(page)*5+5]
    attributes = {'static': static,
                  'current_page': page,
                  'older': int(page)+1,
                  'newer': int(page)-1,
                  'latest_entry_list': latest_entry_list}
    # TODO: refactor this!
    if (int(page) != 0):
        logging.debug("is not first page - adding newer")
        attributes.update(newer_page=True)
    if (int(page) != int(last_page)):
        logging.debug("is not last page - adding older")
        attributes.update(older_page=True)
    logging.info(attributes)
    
    # the context_instance will make sure that the defaultW
    # TEMPLATE_CONTEXT_PROCESSORS are executed, among which
    # the django.core.context_processors.media.  That way
    # the MEDIA_URL will become part of the session
    return render_to_response('index.html', 
                              attributes,
                              context_instance=RequestContext(request))

#@guest_allowed
def detail(request, id):
    static = get_static()
    static['title'] = Static.objects.get(name="index.title").value
    static['header'] = Static.objects.get(name="index.header").value
    entry = get_object_or_404(Entry, pk=id)
    return render_to_response('detail.html', 
                              {'static': static,
                               'entry': entry},
                               context_instance=RequestContext(request))
    
def tags(request, tag):
    static = get_static()
    static['title'] = Static.objects.get(name="tags.title").value
    latest_entry_list = Entry.objects.filter(tags__pk=tag).reverse()
    try:
        tag = Tag.objects.get(id=tag)
        # TODO: refactor this!
        static['header'] = str(latest_entry_list.count()) + " entries tagged with '" + tag.tag + "'"
    except Tag.DoesNotExist:
        static['header'] = "Tag with id " + tag + " not found."
    return render_to_response('index.html', 
                              {'current_page': 1,
                               'older': 1,
                               'newer': 1,
                               'static': static,
                               'latest_entry_list': latest_entry_list},
                              context_instance=RequestContext(request))
    
