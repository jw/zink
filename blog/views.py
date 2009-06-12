from django.shortcuts import render_to_response
from django.template import RequestContext

from elevenbits.blog.models import Entry
from elevenbits.menu.models import Menu

def index(request):
    menu_list = Menu.objects.all()
    latest_entry_list = Entry.objects.all()[:5]
    return render_to_response('index.html', 
                              {'host': 'ElevenBits',
                               'title': 'Home',
                               'menu_list': menu_list, 
                               'latest_entry_list': latest_entry_list},
                              context_instance=RequestContext(request))


