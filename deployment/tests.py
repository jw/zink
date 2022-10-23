from datetime import timedelta
from io import StringIO

from django.core.management import CommandError, call_command
from django.template import Context, Template
from django.test import TestCase
from django.utils import formats, timezone
from semantic_version import Version

from deployment.models import Deployment


class DeploymentTestCase(TestCase):
    def test_deployment(self):
        d = Deployment(version=Version("1.2.3"))
        self.assertIn("Version 1.2.3", f"{d}")


class DeploymentTempateTest(TestCase):
    TEMPLATE = Template(
        "{% load deployment %} version: {% version %} | hash: {% hash %} | timestamp: {% timestamp %}"
    )

    def test_no_deployment(self):
        rendered = self.TEMPLATE.render(Context({}))
        self.assertIn("version: n/a", rendered)
        self.assertIn("hash: n/a", rendered)
        self.assertIn("timestamp: n/a", rendered)

    def test_deployment_present(self):
        date = timezone.now()
        formatted = formats.date_format(date, "l, jS F Y, Hi\h\\r\s")  # noqa W605
        Deployment.objects.create(
            version=Version("1.2.3"), hash="abcd", deployment_date=date
        )
        rendered = self.TEMPLATE.render(Context({}))
        self.assertIn("version: 1.2.3", rendered)
        self.assertIn("hash: abcd", rendered)
        self.assertIn(f"timestamp: {formatted}", rendered)


class CommandsTestCase(TestCase):
    def test_deployment_first(self):
        out = StringIO()
        call_command("deployment", stdout=out)
        self.assertIn("First version ever", out.getvalue())
        self.assertIn("for version 0.1.0", out.getvalue())

        out = StringIO()
        call_command("deployment", stdout=out)
        self.assertNotIn("First version ever", out.getvalue())
        self.assertIn("for version 0.1.1", out.getvalue())

    def test_deloyment(self):
        out = StringIO()
        call_command("deployment", stdout=out)
        self.assertIn("First version ever", out.getvalue())
        self.assertIn("new deployment", out.getvalue())
        self.assertIn("for version 0.1.0", out.getvalue())

        out = StringIO()
        call_command("deployment", "--git=.", stdout=out)
        self.assertNotIn("First version ever", out.getvalue())
        self.assertIn("for version 0.1.1", out.getvalue())

        deployment = Deployment.objects.last()
        self.assertEqual(deployment.git, "https://github.com/jw/zink.git")
        self.assertEqual(deployment.branch, "master")
        self.assertEqual(deployment.version, Version("0.1.1"))

        out = StringIO()
        version = Version("3.1.0")
        commit_date = timezone.now() + timedelta(days=1)
        branch = "fubar"
        call_command(
            "deployment",
            "-v 2",
            f"-dv={version}",
            f"-cd={commit_date}",
            f"--branch={branch}",
            stdout=out,
        )
        deployment = Deployment.objects.last()
        self.assertEqual(deployment.version, version)
        self.assertEqual(deployment.commit_date, commit_date)
        self.assertEqual(deployment.branch, branch)
        self.assertIn("zink.git as remote git repo", out.getvalue())

        out = StringIO()
        version = Version("3.1.0")
        deployment_date = timezone.now() + timedelta(days=1)
        hash = "abcde"
        call_command(
            "deployment",
            f"-dv={version}",
            f"--hash={hash}",
            f"-dd={deployment_date}",
            stdout=out,
        )
        deployment = Deployment.objects.last()
        self.assertEqual(deployment.version, version)
        self.assertEqual(deployment.deployment_date, deployment_date)
        self.assertEqual(deployment.hash, hash)

    def test_deloyment_invalid(self):
        with self.assertRaisesRegex(
            CommandError, "invalid is not a valid semantic version."
        ):
            call_command("deployment", "-dv=invalid")
        with self.assertRaisesRegex(CommandError, "invalid is not a valid git url."):
            call_command("deployment", "--git=invalid")
