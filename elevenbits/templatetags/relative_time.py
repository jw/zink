from django import template
from django.template.defaultfilters import pluralize
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from datetime import datetime
from dateutil import parser # http://labix.org/python-dateutil
#from pytz import timezone # http://pytz.sourceforge.net/
from math import floor
 
register = template.Library()

def to_datetime(string):
    """
        Convert a string to a datetime
    """
    try:
        return timezone.make_aware(parse_datetime(string), timezone.get_current_timezone())
    except:
        return string
    
@register.simple_tag
def relative_time(obj):
    """
        Convert datetime objects into relative t
    """
    #dt = to_datetime(obj)
    dt = timezone.make_aware(parse_datetime(obj), timezone.get_current_timezone())
    string = ""
    
    utc = timezone('UTC')
    now = datetime.now(tz = utc)
    diff = float( (now - dt).days * 86400 + (now - dt).seconds )
    if( diff <= 30 * 60 ): # the difference is 30 seconds or less
        string = 'now'
    else:
        string = 'about '
        t = {
            'year': 0,
            'month': 0,
            'week': 0,
            'day': 0,
            'hour': 0,
            'minute': 0,
        }
        t['year']   = floor( diff / float(31536000) ) # assume 365 days in a year
        t['month']  = floor( ( diff - ( t['year'] * float(31536000) ) ) / float(2592000) ) # assume a month is 30 days
        t['week']   = floor( ( diff - ( t['year'] * float(31536000) ) - ( t['month'] * float(2592000) ) ) / float(604800) )
        t['day']    = floor( ( diff - ( t['year'] * float(31536000) ) - ( t['month'] * float(2592000) ) - ( t['week'] * float(604800) ) ) / float(86400) )
        t['hour']   = floor( ( diff - ( t['year'] * float(31536000) ) - ( t['month'] * float(2592000) ) - ( t['week'] * float(604800) ) - ( t['day'] * float(86400) ) ) / float(3600) )
        t['minute'] = round( ( diff - ( t['year'] * float(31536000) ) - ( t['month'] * float(2592000) ) - ( t['week'] * float(604800) ) - ( t['day'] * float(86400) ) - ( t['hour'] * float(3600) ) ) / float(60) )
        for unit in t:
            t[unit] = int(t[unit])

        if t['year']:
            string += u'%d %s, ' % (t['year'], pluralize(t['year'], 'year,years'))
            if t['month']:
                string += u'%d %s, ' % (t['month'], pluralize(t['month'], 'month,months'))
            elif t['week']:
                string += u'%d %s, ' % (t['week'], pluralize(t['week'], 'week,weeks'))
            elif t['day']:
                string += u'%d %s, ' % (t['day'], pluralize(t['day'], 'day,days'))
        elif t['month']:
            string += u'%d %s, ' % (t['month'], pluralize(t['month'], 'month,months'))
            if t['week']:
                string += u'%d %s, ' % (t['week'], pluralize(t['week'], 'week,weeks'))
            elif t['day']:
                string += u'%d %s, ' % (t['day'], pluralize(t['day'], 'day,days'))
        elif t['week']:
            string += u'%d %s, ' % (t['week'], pluralize(t['week'], 'week,weeks'))
            if t['day']:
                string += u'%d %s, ' % (t['day'], pluralize(t['day'], 'day,days'))
        elif t['day']:
            string += u'%d %s, ' % (t['day'], pluralize(t['day'], 'day,days'))
        elif t['hour']:
            string += u'%d %s, ' % (t['hour'], pluralize(t['hour'], 'hour,hours'))
            if t['hour'] < 13 and t['minute']:
                string += u'%d %s, ' % (t['minute'], pluralize(t['minute'], 'minute,minutes'))
        elif t['minute']:
            string += u'%d %s, ' % (t['minute'], pluralize(t['minute'], 'minute,minutes'))
        
        string = string.rstrip(', ') + ' ago'
        string = ' and '.join( string.rsplit(', ') )

    return string
    
register.filter(relative_time)