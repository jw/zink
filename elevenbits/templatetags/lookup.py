import logging

from django import template

logger = logging.getLogger("elevenbits")

register = template.Library()


@register.filter(name="lookup")
def lookup(dictionary: dict, key: str) -> str:
    """Returns the value for a key."""
    logger.debug(f"Looking for {key} in {dictionary}...")
    return dictionary.get(key) if key in dictionary else "Not found!"
