from elevenbits.static.models import Static
from elevenbits.deployment.models import Deployment

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404


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

    static = dict()
    static['host'] = Static.objects.get(name="header.host").value
    static['description'] = Static.objects.get(name="header.description").value
    static['title'] = Static.objects.get(name="contact.title").value

    deployment = get_deployment()

    attributes = {'static': static,
                  'deployment': deployment}

    return render_to_response('contact.html',
                              attributes,
                              context_instance=RequestContext(request))
