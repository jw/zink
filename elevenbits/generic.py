
import logging

from django.core.exceptions import ObjectDoesNotExist

from blog.models import Static

logger = logging.getLogger("elevenbits")


def get_assets(*keys, prefix=None):
    """Get generic assets.
    :param keys: the keys to be retrieved
    """
    try:
        assets = {'copyright': Static.objects.get(name="copyright").value,
                  'title': Static.objects.get(name="title").value,
                  'rero': Static.objects.get(name='rero').value}
        if prefix:
            for static in Static.objects.filter(name__startswith=prefix):
                assets[static.name] = static.value
        for key in keys:
            assets[key] = Static.objects.get(name=key).value
        return assets
    except Static.DoesNotExist as e:
        raise ObjectDoesNotExist("Could not find some of the assets!")
