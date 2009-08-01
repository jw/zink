from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from elevenbits.blog.models import Tag
from elevenbits.menu.models import Menu
from elevenbits.page.models import Page

def index(request):
    page = Page.objects.get(title="ElevenBits")
    menu_list = Menu.objects.all()
    page.header = "About"
    return render_to_response('base.html', 
                              {'page': page},
                              context_instance=RequestContext(request))
    