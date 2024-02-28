import markdown as markdownify
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
@stringfilter
def markdown(value: str) -> str:
    md = markdownify.Markdown(extensions=["fenced_code", "tables", "codehilite"])
    return mark_safe(md.convert(value))
