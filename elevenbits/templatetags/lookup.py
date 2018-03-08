from django import template

register = template.Library()


@register.filter(name='lookup')
def lookup(dictionary, key):
    """Returns the value for a key."""
    return dictionary.get(key)
