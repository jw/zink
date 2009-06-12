"""
Creates a template tag called {% revision %} that returns the current svn version.
Requires svnversion.
"""
 
import sys, os
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), "../../"))
from django import template
from templatetags import REVISION
 
register = template.Library()

@register.simple_tag
def revision():
    """
        displays the revision number
        {% revision %}
    """
    return REVISION
