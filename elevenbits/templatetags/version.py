
#
# Copyright (C) 2013-2014 Jan Willems (ElevenBits)
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

import pkg_resources

from django import template

register = template.Library()


@register.simple_tag
def version(module):
    """
        displays the version number of the given module
        {% version("django") %}
    """
    try:
        version = pkg_resources.get_distribution(module).version
    except pkg_resources.DistributionNotFound:
        version = "unknown"

    return version

register.filter(version)
