from elevenbits.static.models import Static
from elevenbits.index.models import Image, Believe, About, Tool, Client, Link
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

def contact(request):

    static = {}
    static['copyright'] = Static.objects.get(name="copyright").value
    static['title'] = Static.objects.get(name="elevenbits").value
    static['header'] = Static.objects.get(name="contact.header").value

    slider_images = Image.objects.filter(types__name="slider")

    # selects a believe, a tool or an about message at random
    believe = Believe.objects.order_by('?')[0]
    tool = Tool.objects.order_by('?')[0]
    about = About.objects.order_by('?')[0]

    # bottom part
    static['message'] = Static.objects.get(name="about.message").value
    links = Link.objects.all().order_by('description')
    deployment = get_deployment()

    attributes = {'static': static,
                  'slider_images': slider_images,
                  'believe': believe,
                  'tool': tool,
                  'about': about,
                  'links': links,
                  'deployment': deployment}

    return render_to_response('contact.html',
                              attributes,
                              context_instance=RequestContext(request))