from unittest import TestCase

from django.template import Context, Template


def render_template(string: str) -> str:
    return Template(string).render(Context())


class VersionTest(TestCase):
    def test_version_python(self):
        rendered = render_template("{% load version %}" "{% version 'python' %}")
        self.assertEqual(rendered, "3.11.1")

    def test_version_django(self):
        rendered = render_template("{% load version %}" "{% version 'django' %}")
        self.assertEqual(rendered, "4.1.7")

    def test_version_invalid(self):
        rendered = render_template(
            "{% load version %}" "{% version 'djangofoobar42' %}"
        )
        self.assertEqual(rendered, "unknown")
