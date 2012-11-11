from django import template
from django.template.defaultfilters import pluralize
from django.utils import timezone

register = template.Library()

@register.simple_tag
def relative_time(obj):
    """
        Convert datetime objects into relative t
    """
    
    now = timezone.now()
    difference = now - obj
    
    # seconds
    HALF_MINUTE = 30
    MINUTE = 60
    TWO_MINUTES = 2 * MINUTE
    HOUR = 60 * MINUTE
    TWO_HOURS = 2 * HOUR
    ONE_DAY = 24 * HOUR
    FOURTY_EIGHT_HOURS = 48 * HOUR
    
    # days
    ONE_WEEK = 7
    THREE_WEEKS = 3 * ONE_WEEK
    ONE_MONTH = 4 * ONE_WEEK
    THREE_MONTHS = 3 * ONE_MONTH
    FIFTEEN_MONTHS = 15 * ONE_MONTH
    ONE_YEAR = 365
    
    string = ''
    if (difference.days < 2):
        if (difference.seconds < HALF_MINUTE):
            string = 'moments ago'
        elif (difference.seconds < TWO_MINUTES):
            string = str(difference.seconds) + ' seconds ago'
        elif (difference.seconds < TWO_HOURS):
            string = str(difference.seconds / MINUTE) + ' minutes ago'
        elif (difference.seconds < FOURTY_EIGHT_HOURS):
            string = str(difference.seconds / HOUR) + ' hours ago'
        else:
            string = str(difference.seconds / ONE_DAY)  + ' days ago'
    else:
        if (difference.days < THREE_WEEKS):
            string = str(difference.days)  + ' days ago'
        elif (difference.days < THREE_MONTHS):
            string = str(difference.days / ONE_WEEK)  + ' weeks ago'
        elif (difference.days < FIFTEEN_MONTHS):
            string = str(difference.days / ONE_MONTH) + ' months ago'
        else:
            string = str(difference.days / ONE_YEAR) + ' years ago'
    return string
    
register.filter(relative_time)