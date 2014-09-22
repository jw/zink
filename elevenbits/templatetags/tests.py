
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

from django.test import TestCase
from django.test.client import Client


class DeploymentTest(TestCase):

    fixtures = ['fixtures/static', 'fixtures/blog', 'fixtures/treemenus']

    def setUp(self):
        self.client = Client()

    def test_details(self):
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 200)
