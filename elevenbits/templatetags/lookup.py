from django import template
import logging

logger = logging.getLogger("elevenbits")

register = template.Library()


@register.filter(name='lookup')
def lookup(dictionary, key):
    """Returns the value for a key."""
    logger.info(f'Looking for {key} in {dictionary}...')
    return dictionary.get(key)
