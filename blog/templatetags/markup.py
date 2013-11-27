
#
# Zink
#

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from markdown import markdown

register = template.Library()


@register.filter
@stringfilter
def markup(value):
    """Do the markup."""
    try:
        res = markdown(value, extensions=['codehilite'])
    except Exception as e:
        print(e)
        print(u'value="%s"' % value)
        res = value
    return mark_safe(res)
