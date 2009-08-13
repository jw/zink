from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from elevenbits.blog.models import Tag
from elevenbits.menu.models import Menu
from elevenbits.static.models import Static

def index(request):
    static = {}
    static['title'] = Static.objects.get(name="about.title").value
    static['header'] = Static.objects.get(name="about.header").value
    static['text'] = Static.objects.get(name="about.text").value
    static['deployment_time'] = Static.objects.get(name="deployment.time").value
    static['copyright'] = Static.objects.get(name="copyright").value
    menu_list = Menu.objects.all()
    return render_to_response('about.html', 
                              {'static': static,
                               'menu_list': menu_list},
                              context_instance=RequestContext(request))
    