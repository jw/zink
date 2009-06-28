from django import template
register = template.Library()

from guest import display_username as display_username_func
from guest import is_a_guest as is_a_guest_func

@register.filter
def display_username(user):
    return display_username_func(user)

@register.filter
def is_a_guest(user):
    return is_a_guest_func(user)
