from django.test import TestCase

from zink.templatetags.lookup import lookup
from zink.templatetags.markdownify import markdown
from zink.templatetags.version import version


class VersionTestCase(TestCase):

    def test_version_python(self):
        self.assertEqual(version("python"), "3.9.9")

    def test_version_django(self):
        self.assertEqual(version("Django"), "3.2.9")

    def test_version_unknown(self):
        self.assertEqual(version("foobar"), "unknown")


class LookupTestCase(TestCase):

    def setUp(self):
        self.d = {"abd": "def", "foo": "bar"}

    def test_lookup_foo(self):
        self.assertEqual(lookup(self.d, "foo"), "bar")

    def test_version_django(self):
        self.assertEqual(lookup(self.d, "explosion"), "Not found!")


class MarkdownifyTestCase(TestCase):

    def test_markdown_python(self):
        text = """
    ::::python
        def hello():
            foo = "bar"
            print(f"{foo}")
"""
        result = markdown(text)
        self.assertTrue("<span class=\"k\">def</span>" in result)
        self.assertTrue("<span class=\"sa\">f</span>" in result)
        self.assertTrue("<span class=\"s2\">&quot;</span>" in result)

    def test_markdown_html(self):
        text = """
### header

 * one
 * two

Some `a = 1 + 2` expressions could be **important**, or _italic_.
"""
        result = markdown(text)
        self.assertTrue("<h3>header</h3>" in result)
        self.assertTrue("<li>one</li>" in result)
        self.assertTrue("<code>a = 1 + 2</code>" in result)
        self.assertTrue("<strong>important</strong>" in result)
        self.assertTrue("<em>italic</em>" in result)
