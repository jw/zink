import os
from importlib import metadata
from unittest import TestCase, mock

from django.template import Context, Template


def render_template(string: str) -> str:
    return Template(string).render(Context())


class VersionTest(TestCase):
    def test_version_python(self):
        rendered = render_template("{% load version %}{% version 'python' %}")
        self.assertEqual(rendered, "3.14.2")

    def test_version_django(self):
        rendered = render_template("{% load version %}{% version 'django' %}")
        self.assertEqual(rendered, metadata.version("django"))

    def test_version_invalid(self):
        rendered = render_template("{% load version %}{% version 'djangofoobar42' %}")
        self.assertEqual(rendered, "unknown")

    def test_version_hash_uses_render_env_var_when_set(self):
        with mock.patch.dict("os.environ", {"RENDER_GIT_COMMIT": "abcdef0123456789"}):
            rendered = render_template("{% load version %}{% version 'hash' %}")
        self.assertEqual(rendered, "abcdef01")

    def test_version_hash_falls_back_to_local_checkout(self):
        with mock.patch.dict(os.environ):
            os.environ.pop("RENDER_GIT_COMMIT", None)
            rendered = render_template("{% load version %}{% version 'hash' %}")
        self.assertRegex(rendered, r"^([0-9a-f]{7,8}|unknown)$")
