import pkg_resources

from django import template

register = template.Library()


@register.simple_tag
def version(module):
    """
        displays the version number of the given module
        {% version("django") %}
    """
    try:
        version = pkg_resources.get_distribution(module).version
    except pkg_resources.DistributionNotFound:
        version = "unknown"

    return version

register.filter(version)
