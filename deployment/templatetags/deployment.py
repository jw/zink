from django import template
from django.utils import formats

from deployment.models import Deployment

register = template.Library()


@register.simple_tag
def timestamp(date_format="l, jS F Y, Hi\h\\r\s"):  # noqa: W605
    result = "n/a"
    deployment = Deployment.objects.last()
    if deployment:
        return f"{formats.date_format(deployment.deployment_date, date_format)}"
    return result


@register.simple_tag
def version():
    result = "n/a"
    deployment = Deployment.objects.last()
    if deployment:
        return f"{deployment.version}"
    return result


@register.simple_tag
def hash(short=True):
    result = "n/a"
    deployment = Deployment.objects.last()
    if deployment:
        return f"{deployment.hash[:7]}" if short else f"{deployment.hash}"
    return result


register.filter(timestamp)
register.filter(version)
register.filter(hash)
