from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from elevenbits.static.models import Static
from elevenbits.deployment.models import Deployment 


# get latest deployment
def get_deployment():
    deployment = {}
    try:
        last = Deployment.objects.all().reverse()[0]
        deployment['tag'] = last.tag
        deployment['timestamp'] = last.timestamp
        deployment['version'] = last.version
        deployment['deployer'] = last.deployer
    except IndexError:
        from datetime import datetime
        deployment['tag'] = "unknown"
        deployment['timestamp'] = datetime.now()
        deployment['version'] = "unknown"
        deployment['deployer'] = "unknown"
    return deployment


def get_static():
    static = {}
    static['deployment_time'] = Static.objects.get(name="deployment.time").value
    static['copyright'] = Static.objects.get(name="copyright").value
    return static


def about(request):
    deployment = get_deployment()
    static = get_static()
    static['title'] = Static.objects.get(name="about.title").value
    static['header'] = Static.objects.get(name="about.header").value
    return render_to_response('elevenbits/about.html', 
                              {
                                 'static': static, 
                                 'deployment': deployment,
                              },
                              context_instance=RequestContext(request))

def contact(request):
    deployment = get_deployment()
    static = get_static()
    static['title'] = Static.objects.get(name="contact.title").value
    static['header'] = Static.objects.get(name="contact.header").value
    return render_to_response('elevenbits/contact.html', 
                              {
                                  'static': static,
                                  'deployment': deployment,
                              },
                              context_instance=RequestContext(request))

def clients(request):
    deployment = get_deployment()
    static = get_static()
    static['title'] = Static.objects.get(name="clients.title").value
    static['header'] = Static.objects.get(name="clients.header").value
    return render_to_response('elevenbits/clients.html', 
                              {
                                 'static': static,
                                 'deployment': deployment,
                              },
                              context_instance=RequestContext(request))

def projects(request):
    deployment = get_deployment()
    static = get_static()
    static['title'] = Static.objects.get(name="projects.title").value
    static['header'] = Static.objects.get(name="projects.header").value
    return render_to_response('elevenbits/projects.html', 
                              {
                                 'static': static,
                                 'deployment': deployment,
                              },
                              context_instance=RequestContext(request))
    