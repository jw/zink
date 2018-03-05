
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

from django.shortcuts import render

from util.generic import get_assets
from util.deployment import get_deployment

from blog.models import Entry

import logging
logger = logging.getLogger("elevenbits")


def home(request):
    """Show the home page."""

    assets = get_assets("index.header")
    deployment = get_deployment()

    entry_list = Entry.objects.filter(active=True).reverse()
    logger.error("Retrieved %s blog entries." % len(entry_list))

    try:
        entry = entry_list.first()
    except IndexError:
        entry = None

    attributes = {'deployment': deployment,
                  'entry': entry,
                  'entries': entry_list[1:],
                  'assets': assets}

    return render(request, 'index.html', attributes)
