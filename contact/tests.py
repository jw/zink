
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
from django.core.urlresolvers import reverse

import logging
logger = logging.getLogger('elevenbits')


class FormTest(TestCase):

    fixtures = ['static', 'contact', 'treemenus', 'menu_extras']

    def setUp(self):
        pass

    def test_get_contact_index_page(self):
        """Tests a valid contact post to the site."""
        c = Client()
        response = c.get(reverse('contact:contact'))
        self.assertContains(response,
                            '<h3 id="form">',
                            status_code=200)
        self.assertContains(response,
                            '<title>Contact Us - elevenbits</title>',
                            status_code=200)

    def test_current_menu_selection(self):
        """Tests the current menu selection."""
        c = Client()
        response = c.get(reverse('contact:contact'))
        self.assertContains(response, '<li class="current">', status_code=200)

    def test_valid_post(self):
        """Tests a valid contact post to the site."""
        c = Client()
        response = c.post(reverse('contact:contact'),
                          {'name': 'test',
                           'email': 'jw@elevenbits.com',
                           'subject': '[TEST]',
                           'message': 'Test message.'})
        self.assertEquals(response.status_code, 302)

    def test_no_name_post(self):
        """Tests post of a form without a name."""
        c = Client()
        response = c.post(reverse('contact:contact'),
                          {'email': 'jw@elevenbits.com',
                           'subject': '[TEST]',
                           'message': 'Test message.'})
        self.assertContains(response, '<p class="error">', status_code=200)

    def test_no_email_post(self):
        """Tests post of a form without an email."""
        c = Client()
        response = c.post(reverse('contact:contact'),
                          {'name': 'test',
                           'subject': '[TEST]',
                           'message': 'Test message.'})
        self.assertContains(response, '<p class="error">', status_code=200)

    def test_no_message_post(self):
        """Tests post of a form without a message."""
        c = Client()
        response = c.post(reverse('contact:contact'),
                          {'name': 'test',
                           'subject': '[TEST]',
                           'email': 'jw@elevenbits.com'})
        self.assertContains(response, '<p class="error">', status_code=200)

    def test_spam_post(self):
        """Tests post of a form with spam in it."""
        c = Client()
        response = c.post(reverse('contact:contact'),
                          {'name': 'test',
                           'subject': '[TEST]',
                           'email': 'jw@elevenbits.com',
                           'spam': 'this is spam',
                           'message': 'Hello there!'})
        self.assertContains(response, '<p class="error">', status_code=200)


class DataTest(TestCase):

    # TODO: implement this test!
    def test_no_data(self):
        """When no data are available, a mail must be sent"""
        pass
