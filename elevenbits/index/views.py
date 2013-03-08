from elevenbits.static.models import Static
from elevenbits.index.models import Image, Believe, About, Tool, Client, Link

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.conf import settings

def index(request):

    static = {}
    static['copyright'] = Static.objects.get(name="copyright").value
    static['title'] = Static.objects.get(name="index.title").value
    static['header'] = Static.objects.get(name="index.header").value

    slider_images = Image.objects.filter(types__name="slider")

    # selects one from a list at random
    believe = Believe.objects.order_by('?')[0]
    tool = Tool.objects.order_by('?')[0]
    about = About.objects.order_by('?')[0]

    # get 6 random clients
    clients = Client.objects.all().order_by('?')[:6]
    width = 0
    for client in clients:
        width += client.image.width + settings.CLIENT_LOGO_MARGIN

    # bottom part
    static['message'] = Static.objects.get(name="about.message").value
    links = Link.objects.all().order_by('description')

    attributes = {'static': static,
                  'believe': believe,
                  'tool': tool,
                  'about': about,
                  'links': links,
                  'slider_images': slider_images,
                  'clients': clients,
                  'width': width}

    return render_to_response('index.html',
                              attributes,
                              context_instance=RequestContext(request))
