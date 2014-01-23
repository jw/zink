
#
# Zink
#

from django.test import TestCase
from django.test.client import Client

from elevenbits.deployment.models import Deployment
from elevenbits.static.models import Static
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
        self.assertIn("404 message", str(response))

    def test500(self):
        client = Client()
        response = client.get("/500")
        self.assertIn("500 message", str(response))

    def testRobots(self):
        client = Client()
        response = client.get("/robots.txt")
        self.assertIn("User-agent: *", str(response))

    def test_something(self):
        pass
