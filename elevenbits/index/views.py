from elevenbits.static.models import Static
from elevenbits.index.models import Image, Believe, About, Tool, Project, Client, Link
from elevenbits.deployment.models import Deployment

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.conf import settings

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

def index(request):

    static = {}
    static['copyright'] = Static.objects.get(name="copyright").value
    static['title'] = Static.objects.get(name="elevenbits").value
    static['header'] = Static.objects.get(name="home.header").value

    slider_images = Image.objects.filter(types__name="slider")

    # selects a believe, a tool and an about message at random
    believe = Believe.objects.order_by('?')[0]
    tool = Tool.objects.order_by('?')[0]
    about = About.objects.order_by('?')[0]

    # gets 6 random clients
    clients = Client.objects.all().order_by('?')[:6]
    # the width calculation is a small hack to center the clients
    width = 0
    for client in clients:
        width += client.logo.width + settings.CLIENT_LOGO_MARGIN

    # bottom part
    static['message'] = Static.objects.get(name="about.message").value
    links = Link.objects.all().order_by('description')
    deployment = get_deployment()

    attributes = {'static': static,
                  'slider_images': slider_images,
                  'believe': believe,
                  'tool': tool,
                  'about': about,
                  'clients': clients,
                  'width': width,
                  'links': links,
                  'deployment': deployment}

    return render_to_response('index.html',
                              attributes,
                              context_instance=RequestContext(request))

def clients(request):
    static = {}
    static['copyright'] = Static.objects.get(name="copyright").value
    static['title'] = Static.objects.get(name="elevenbits").value
    static['header'] = Static.objects.get(name="home.header").value

    # selects a believe, a tool and an about message at random
    clients = Client.objects.all()

    # bottom part
    static['message'] = Static.objects.get(name="about.message").value
    links = Link.objects.all().order_by('description')
    deployment = get_deployment()

    attributes = {'static': static,
                  'clients': clients,
                  'links': links,
                  'deployment': deployment}

    return render_to_response('clients.html',
                              attributes,
                              context_instance=RequestContext(request))


def projects(request):
    static = {}
    static['copyright'] = Static.objects.get(name="copyright").value
    static['title'] = Static.objects.get(name="elevenbits").value
    static['header'] = Static.objects.get(name="home.header").value

    # selects a believe, a tool and an about message at random
    projects = Project.objects.all()

    # bottom part
    static['message'] = Static.objects.get(name="about.message").value
    links = Link.objects.all().order_by('description')
    deployment = get_deployment()

    attributes = {'static': static,
                  'projects': projects,
                  'links': links,
                  'deployment': deployment}

    return render_to_response('elevenbits/projects.html',
                              attributes,
                              context_instance=RequestContext(request))

