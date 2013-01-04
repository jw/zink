import pkg_resources

from django import template

register = template.Library()

@register.simple_tag
def version(module):
    """
        displays the version number of the given module
        {% version("django" %}
    """
    version = "unknown"
    try:
        version = pkg_resources.get_distribution(module).version
    except pkg_resources.DistributionNotFound:
        pass

    return version

register.filter(version)