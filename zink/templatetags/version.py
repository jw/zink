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
        python_version = sys.version_info
        return f"{python_version[0]}.{python_version[1]}.{python_version[2]}"
    else:
        try:
            package_version = pkg_resources.get_distribution(module).version
        except pkg_resources.DistributionNotFound:
            package_version = "unknown"

    return package_version


register.filter(version)
