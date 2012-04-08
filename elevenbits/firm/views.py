from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from elevenbits.static.models import Static

def get_static():
    static = {}
    static['deployment_time'] = Static.objects.get(name="deployment.time").value
    static['copyright'] = Static.objects.get(name="copyright").value
    return static

def about(request):
    static = get_static()
    static['title'] = Static.objects.get(name="about.title").value
    static['header'] = Static.objects.get(name="about.header").value
    return render_to_response('elevenbits/about.html', 
                              {'static': static, },
                              context_instance=RequestContext(request))

def contact(request):
    static = get_static()
    static['title'] = Static.objects.get(name="contact.title").value
    static['header'] = Static.objects.get(name="contact.header").value
    return render_to_response('elevenbits/contact.html', 
                              {'static': static, },
                              context_instance=RequestContext(request))

def clients(request):
    static = get_static()
    static['title'] = Static.objects.get(name="clients.title").value
    static['header'] = Static.objects.get(name="clients.header").value
    return render_to_response('elevenbits/clients.html', 
                              {'static': static, },
                              context_instance=RequestContext(request))

def projects(request):
    static = get_static()
    static['title'] = Static.objects.get(name="projects.title").value
    static['header'] = Static.objects.get(name="projects.header").value
    return render_to_response('elevenbits/projects.html', 
                              {'static': static, },
                              context_instance=RequestContext(request))
    