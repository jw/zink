#
# Copyright (c) 2013-2016 Jan Willems (ElevenBits)
#
# This file is part of Zink.
#
# Zink is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Zink is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Zink.  If not, see <http://www.gnu.org/licenses/>.
#

from django import template
from django.utils import timezone

register = template.Library()


@register.simple_tag
def relative_time(obj: any) -> str:
    """
    Convert datetime objects into relative time.
    """

    if isinstance(obj, str):
        return "unknown time ago"

    now = timezone.now()
    difference = now - obj

    # seconds
    half_minute = 30
    minute = 60
    two_minutes = 2 * minute
    hour = 60 * minute
    two_hours = 2 * hour
    one_day = 24 * hour
    forty_eight_hours = 48 * hour

    # days
    one_week = 7
    three_weeks = 3 * one_week
    one_month = 4 * one_week
    three_months = 3 * one_month
    fifteen_months = 15 * one_month
    one_year = 365

    # TODO: use pluralise to handle 1 second vs 2+ secondS
    if difference.days < 2:
        if difference.seconds < half_minute:
            string = "moments ago"
        elif difference.seconds < two_minutes:
            string = str(difference.seconds) + " seconds ago"
        elif difference.seconds < two_hours:
            string = str(difference.seconds // minute) + " minutes ago"
        elif difference.seconds < forty_eight_hours:
            string = str(difference.seconds // hour) + " hours ago"
        else:
            string = str(difference.seconds // one_day) + " days ago"
    else:
        if difference.days < three_weeks:
            string = str(difference.days) + " days ago"
        elif difference.days < three_months:
            string = str(difference.days // one_week) + " weeks ago"
        elif difference.days < fifteen_months:
            string = str(difference.days // one_month) + " months ago"
        else:
            string = str(difference.days // one_year) + " years ago"
    return string


register.filter(relative_time)
