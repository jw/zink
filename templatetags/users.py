from django import template

from django.contrib.sessions.models import Session

from elevenbits.guest.models import Guest

from datetime import datetime, timedelta

register = template.Library()

def get_authenticated_users():
    now = datetime.now()
    # TODO: make the 2 part of the settings.py
    difference = timedelta(minutes=-2)
    time = now + difference
    return Session.objects.filter(expire_date__gte=time).count()

def get_unauthenticated_users():
    now = datetime.now() 
    # TODO: make the 2 part of the settings.py
    difference = timedelta(minutes=-2)
    time = now + difference
    return Guest.objects.filter(last_used__gte=time).count()

def get_all_users():
    return str(get_authenticated_users() + get_unauthenticated_users())

@register.simple_tag
def authenticated_users():
    """
        Displays the number of all authenticated users that are currently 
        logged in. 
        {% authenticated_users %}
    """
    return get_authenticated_users()

@register.simple_tag
def unauthenticated_users():
    """
        Displays the number of all unauthenticated users that are currently 
        visiting the site. 
        {% guests %}
    """
    return get_unauthenticated_users()

@register.simple_tag
def all_users():
    """
        Displays the number of all users that are currently viewing the site.
    """
    return get_all_users()
    