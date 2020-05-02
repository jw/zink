import pkg_resources
import sys
from django import template

register = template.Library()


@register.simple_tag
def version(module):
    """
        Display the version number of the given module
        {% version("django") %}
    """
    if module == "python":
        return "{}.{}.{}".format(sys.version_info[0],
                                 sys.version_info[1],
                                 sys.version_info[2])
    else:
        try:
            version = pkg_resources.get_distribution(module).version
        except pkg_resources.DistributionNotFound:
            version = "unknown"

    return version


register.filter(version)
