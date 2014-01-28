
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

from django.utils import unittest
from elevenbits.static.models import Static


class StaticTestCase(unittest.TestCase):

    def setUp(self):
        self.foo = Static.objects.create(name="foo", value="FOO")
        self.bar = Static.objects.create(name="BAR", value="bar")

    def test_statics(self):
        """Tesing foo and bar."""
        self.assertEqual(self.foo.name, "foo")
        self.assertEqual(self.bar.value, "bar")
