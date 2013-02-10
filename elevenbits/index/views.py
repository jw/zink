from elevenbits.static.models import Static
from elevenbits.index.models import Image

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

def get_static():
    static = {}
    static['copyright'] = Static.objects.get(name="copyright").value
    return static

def index(request):

    static = get_static()

    static['title'] = Static.objects.get(name="index.title").value
    static['header'] = Static.objects.get(name="index.header").value

    slider_images = Image.objects.filter(types__name="slider")
    client_images = Image.objects.filter(types__name="client")

    attributes = {'static': static,
                  'slider_images': slider_images,
                  'client_images': client_images
    }

    return render_to_response('index.html',
        attributes,
        context_instance=RequestContext(request))
