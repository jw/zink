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

import logging

from static.models import Static

logger = logging.getLogger("elevenbits")


def get_assets(*keys):
    """Get generic assets.
    :param keys: the keys to be retrieved
    """
    try:
        assets = {'copyright': Static.objects.get(name="copyright").value,
                  'title': Static.objects.get(name="title").value,
                  'rero': Static.objects.get(name='rero').value}
        for key in keys:
            assets[key] = Static.objects.get(name=key).value
        return assets
    except Static.DoesNotExist as e:
        print(f"Oops {e}")
        # raise Static.DoesNotExist("Could not find assets!", Static, e)
