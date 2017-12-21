
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

from static.models import Static

import logging
logger = logging.getLogger("elevenbits")


def get_static(name):
    """Get generic assets information."""
    static = {}
    static['copyright'] = Static.objects.get(name="copyright").value
    static['host'] = Static.objects.get(name="elevenbits").value
    static['title'] = Static.objects.get(name=name).value
    return static
