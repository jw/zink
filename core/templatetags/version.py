import sys
from importlib import metadata
from importlib.metadata import PackageNotFoundError

from django import template

register = template.Library()


@register.simple_tag
def version(module: str) -> str:
    """
    Display the version number of the given module
    {% version("django") %}
    """
    if module == "python":
        return f"{sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}"
    else:
        try:
            version = metadata.version(module)
        except PackageNotFoundError:
            version = "unknown"

    return version


register.filter(version)
