from django import template
from django.template.defaultfilters import pluralize
from django.utils import timezone
from django.utils.dateparse import parse_datetime

register = template.Library()

@register.simple_tag
def relative_time(obj):
    """
        Convert datetime objects into relative t
    """
    #dt = to_datetime(obj)
    print("deployment time: " + str(obj))
    import os
    print(os.environ['TZ'])
    now = timezone.now()
    print("now: " + str(now))
    difference = now - obj
    print("Difference: " + str(difference))
    HALF_MINUTE = 30
    MINUTE = 60
    TWO_MINUTES = 2 * MINUTE
    HOUR = 60 * MINUTE
    TWO_HOURS = 2 * HOUR
    ONE_DAY = 24 * HOUR
    ONE_WEEK = 7 * ONE_DAY
    THREE_WEEKS = 3 * ONE_WEEK
    ONE_MONTH = 4 * ONE_WEEK
    THREE_MONTHS = 3 * ONE_MONTH
    FIFTEEN_MONTHS = 3 * ONE_MONTH
    ONE_YEAR = 365 * ONE_DAY
    FOURTY_EIGHT_HOURS = 48 * HOUR
    string = ''
    print("days: " + str(difference.days))
    print("seconds: " + str(difference.seconds))
    if (difference.seconds < HALF_MINUTE):
        string = 'moments ago'
    elif (difference.seconds < TWO_MINUTES):
        string = 'about ' + difference.seconds + ' seconds ago'
    elif (difference.seconds < TWO_HOURS):
        string = 'about ' + difference.seconds / MINUTE + ' minutes ago'
    elif (difference.seconds < FOURTY_EIGHT_HOURS):
        string = 'about ' + str(difference.seconds / HOUR) + ' hours ago'
    elif (difference.seconds < THREE_WEEKS):
        string = 'about ' + difference.seconds / ONE_DAY  + ' days ago'
    elif (difference.seconds < THREE_MONTHS):
        string = 'about ' + difference.seconds / ONE_WEEK  + ' weeks ago'
    elif (difference.seconds < FIFTEEN_MONTHS):
        string = 'about ' + difference.seconds / ONE_MONTH + ' months ago'
    else:
        string = 'about ' + difference.seconds / ONE_YEAR + ' years ago'
    print("result:" + string)
    return string
    
register.filter(relative_time)