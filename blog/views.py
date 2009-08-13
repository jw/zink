from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from elevenbits.blog.models import Entry
from elevenbits.blog.models import Tag
from elevenbits.menu.models import Menu
from elevenbits.page.models import Page
from elevenbits.static.models import Static

from elevenbits.guest.decorators import guest_allowed, login_required

import logging
    
@guest_allowed
def index(request, page=0):
    p = Page.objects.get(title="ElevenBits")
    static = {}
    static['title'] = Static.objects.get(name="index.title").value
    static['header'] = Static.objects.get(name="index.header").value
    static['deployment_time'] = Static.objects.get(name="deployment.time").value
    menu_list = Menu.objects.all()
    logging.debug("total: " + str(Entry.objects.filter(active=True).count()))
    last_page = (Entry.objects.filter(active=True).count() - 1)/5
    logging.debug("0 | page | last_page")
    logging.debug("0 | " + str(page) + " | " + str(last_page))
    latest_entry_list = Entry.objects.filter(active=True).reverse()[int(page)*5:int(page)*5+5]
    attributes = {'static': static,
                  'menu_list': menu_list, 
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

@guest_allowed
def detail(request, id):
    page = Page.objects.get(title="ElevenBits")
    menu_list = Menu.objects.all()
    entry = get_object_or_404(Entry, pk=id)
    page.header = entry.title
    return render_to_response('detail.html', 
                              {'page': page,
                               'menu_list': menu_list, 
                               'entry': entry},
                              context_instance=RequestContext(request))
    
def tags(request, tag):
    page = Page.objects.get(title="ElevenBits")
    menu_list = Menu.objects.all()
    latest_entry_list = Entry.objects.filter(tags__pk=tag).reverse()
    try:
        tag = Tag.objects.get(id=tag)
        # TODO: refactor this!
        page.header = str(latest_entry_list.count()) + " entries tagged with '" + tag.tag + "'"
    except Tag.DoesNotExist:
        page.header = "Tag with id " + tag + " not found."
    return render_to_response('index.html', 
                              {'page': page,
                               'menu_list': menu_list, 
                               'latest_entry_list': latest_entry_list},
                              context_instance=RequestContext(request))
    
