
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

from django.test import TestCase
from django.test.client import Client

from deployment.models import Deployment
from static.models import Static
from treemenus.models import Menu
from treemenus.models import MenuItem
from elevenbits.menu_extras.models import MenuItemExtension

from datetime import datetime

import logging
logger = logging.getLogger('elevenbits')


class ZinkTest(TestCase):

    def setUp(self):
        """First create some statics, and a menu system."""
        # create some statics
        Static(name='header.host', value='host').save()
        Static(name='header.description', value='description').save()
        Static(name='contact.title', value='title').save()
        # create the menu system
        menu = Menu(name='root')
        menu.save()
        home = MenuItem.objects.create(caption="home", parent=menu.root_item)
        blog = MenuItem.objects.create(caption="blog", parent=menu.root_item)
        contact = MenuItem.objects.create(caption="contact",
                                          parent=menu.root_item)
        contact_extra = MenuItemExtension(menu_item=contact,
                                          selected_patterns="/contact")
        contact_extra.save()
        # create a deployment instance
        deployment = Deployment(tag="testtag", version="1.0.0",
                                timestamp=datetime.now(), deployer="unittest")
        deployment.save()

    def test404(self):
        client = Client()
        response = client.get("/this_page_does_not_exist")
        self.assertEqual(response.status_code, 404)

    def test500(self):
        client = Client()
        response = client.get("/500")
        self.assertIn(b'500 message', response.content)

    def testRobots(self):
        client = Client()
        response = client.get("/robots.txt")
        self.assertIn(b'User-agent: *', response.content)
