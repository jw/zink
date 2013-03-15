from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings

from elevenbits.static.models import Static
from elevenbits.index.models import Client, Link

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
    static['message'] = Static.objects.get(name="about.message").value
    static['title'] = Static.objects.get(name="elevenbits").value
    static['header'] = Static.objects.get(name="service.header").value
    static['methodologies_one'] = Static.objects.get(name="service.methodologies_one").value
    static['methodologies_two'] = Static.objects.get(name="service.methodologies_two").value
    return static

def services(request):
    deployment = get_deployment()
    static = get_static()
    # gets 6 random clients
    clients = Client.objects.all().order_by('?')[:6]
    # this is a small hack to center the clients
    width = 0
    for client in clients:
        width += client.image.width + settings.CLIENT_LOGO_MARGIN
    links = Link.objects.all().order_by('description')
    return render_to_response('services.html',
                              {'static': static,
                               'deployment': deployment,
                               'clients': clients,
                               'width': width,
                               'links': links},
                              context_instance=RequestContext(request))
