import logging
import tempfile
from datetime import datetime, timezone
from unittest import skipIf

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.test.client import Client
from django.urls import reverse

from blog.models import Comment, Entry, Image, Static, Tag
from blog.sync import apply_missing, diff_entries, entry_key
from elevenbits.generic import get_assets

# A valid 1x1 transparent PNG, for tests that need a real image file.
ONE_PIXEL_PNG = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
    b"\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
)

logger = logging.getLogger("elevenbits")


class IndexTest(TestCase):
    """Test the home page."""

    fixtures = ["blog"]

    def test_blog(self):
        """Test the home page."""
        client = Client()
        response = client.get("/")
        self.assertContains(response, "I love to cycle.")


class TagTestCase(TestCase):
    """Test the basic tag creation."""

    def setUp(self):
        self.linux = Tag.objects.create(tag="linux")
        self.nginx = Tag.objects.create(tag="nginx")

    def test_tag_creation(self):
        self.assertEqual(self.linux.tag, "linux")
        self.assertEqual(self.nginx.tag, "nginx")


class BlogTest(TestCase):
    """Test all the blog features."""

    fixtures = ["blog"]

    def test_blog(self):
        """Test the full blog."""
        client = Client()
        response = client.get(reverse("blog:blog"))
        self.assertContains(response, "Tag Cloud")
        self.assertContains(response, "/blog")
        self.assertContains(response, "Running on")

    def test_tag(self):
        """Test one tag."""
        client = Client()
        response = client.get(reverse("blog:tag", args=[4]))  # django
        self.assertContains(response, "2 entries tagged with")
        self.assertContains(response, "My first own blog!")
        self.assertContains(response, "Eclipse and Django development setup")
        self.assertContains(response, "Tag Cloud")

    @skipIf(True, "I don't want to run this test yet")
    def test_detail(self):
        """Test one single blog entry."""
        client = Client()
        # get the 'how to access cherokee-admin...' entry
        response = client.get(reverse("blog:detail", args=[21]))
        self.assertContains(response, "Create an SSH tunnel.")

    @skipIf(True, "I don't want to run this test yet")
    def test_page_tag(self):
        """Test the tag pages"""
        client = Client()
        # page 1
        response = client.get(reverse("blog:tagpage", args=[6, 1]))  # linux
        self.assertContains(response, "How to access cherokee-admin")
        self.assertContains(response, "Howto merge PDF documents")
        self.assertContains(response, "How to ask questions the smart way")
        # page 2
        response = client.get(reverse("blog:tagpage", args=[6, 2]))  # linux
        self.assertContains(response, "My first own blog!")
        self.assertContains(response, "Howto create your own Ubuntu")

    @skipIf(True, "I don't want to run this test yet")
    def test_inactive_tag(self):
        """Only active tags must be shown."""
        client = Client()
        response = client.get(reverse("blog:tag", args=[7]))  # python
        self.assertContains(response, "Eclipse and Django development setup")
        self.assertContains(response, "My first own blog!")
        # the inactive one must not be there!
        self.assertNotContains(response, "Temporary entry")

    @skipIf(True, "I don't want to run this test yet")
    def test_markup(self):
        """Make sure the codehilite works."""
        client = Client()
        response = client.get(reverse("blog:detail", args=[21]))
        self.assertContains(
            response, '<div class="codehilite"><pre>' '<span class="gp">'
        )


class HttpErrorHandling(TestCase):
    """Test the Http Error pages."""

    fixtures = ["blog"]

    @skipIf(True, "I don't want to run this test yet")
    def test_404(self):
        """Test the 404 response."""
        client = Client()
        response = client.get("/this_page_does_not_exist")
        self.assertContains(response, "404 message", status_code=404)

    # todo: rename me!
    @skipIf(True, "I don't want to run this test yet")
    def test_404_bis(self):
        """Test the 404 response."""
        client = Client()
        response = client.post("/foobar", data={"q": "Python"})
        self.assertContains(response, "404 message", status_code=404)


class StaticsTestCase(TestCase):
    fixtures = ["blog"]

    def test_statics_are_available(self):
        """Ensure that the default assets are there"""
        logging.info("Trying to get static stuff...")
        rero = Static.objects.get(name="copyright").value
        copyright = (Static.objects.get(name="copyright").value,)
        title = Static.objects.get(name="title").value
        self.assertIsNotNone(rero)
        self.assertIsNotNone(copyright)
        self.assertIsNotNone(title)

    def test_get_statics(self):
        """Get the generic assets and more"""
        assets = get_assets("index.header")
        self.assertIn("rero", assets)
        self.assertIn("copyright", assets)
        self.assertIn("title", assets)
        self.assertIn("index.header", assets)

    def test_get_bigger_statics(self):
        """Get the generic assets and even more"""
        assets = get_assets("index.header", "index.latest")
        self.assertIn("rero", assets)
        self.assertIn("copyright", assets)
        self.assertIn("title", assets)
        self.assertIn("index.header", assets)
        self.assertIn("index.latest", assets)

    def test_get_prefix(self):
        """Get the generic assets and a prefix"""
        assets = get_assets(prefix="index")
        self.assertIn("rero", assets)
        self.assertIn("copyright", assets)
        self.assertIn("title", assets)
        self.assertIn("index.header", assets)
        self.assertIn("index.latest", assets)
        self.assertIn("index.entries", assets)

    def test_get_prefix_and_extra(self):
        """Get the generic assets, a prefix set and an extra"""
        assets = get_assets("contact.country", prefix="index")
        self.assertIn("rero", assets)
        self.assertIn("copyright", assets)
        self.assertIn("title", assets)
        self.assertIn("contact.country", assets)
        self.assertIn("index.header", assets)
        self.assertIn("index.latest", assets)
        self.assertIn("index.entries", assets)

    def test_get_prefix_and_two_extras(self):
        """Get the generic assets, a prefix set and two extras"""
        assets = get_assets("title", "index.header", prefix="contact")
        self.assertIn("rero", assets)
        self.assertIn("copyright", assets)
        self.assertIn("title", assets)
        self.assertIn("index.header", assets)
        self.assertIn("contact.name", assets)


class DiffEntriesTest(TestCase):
    """Test the entry comparison used by the sync_blog_entries command."""

    def test_entry_key_is_title_and_posted(self):
        posted = datetime(2020, 1, 1, tzinfo=timezone.utc)
        entry = Entry(title="Hello", posted=posted)
        self.assertEqual(entry_key(entry), ("Hello", posted))

    def test_matched_entry_present_in_both(self):
        posted = datetime(2020, 1, 1, tzinfo=timezone.utc)
        local = [Entry(title="Shared", posted=posted)]
        dump = [Entry(title="Shared", posted=posted)]

        report = diff_entries(local, dump)

        self.assertEqual([e.title for e in report.matched], ["Shared"])
        self.assertEqual(report.missing, [])
        self.assertEqual(report.local_only, [])

    def test_entry_only_in_dump_is_missing(self):
        posted = datetime(2020, 1, 1, tzinfo=timezone.utc)
        local = []
        dump = [Entry(title="New from dump", posted=posted)]

        report = diff_entries(local, dump)

        self.assertEqual([e.title for e in report.missing], ["New from dump"])
        self.assertEqual(report.matched, [])

    def test_entry_only_locally_is_left_alone(self):
        posted = datetime(2020, 1, 1, tzinfo=timezone.utc)
        local = [Entry(title="Local draft", posted=posted)]
        dump = []

        report = diff_entries(local, dump)

        self.assertEqual([e.title for e in report.local_only], ["Local draft"])
        self.assertEqual(report.missing, [])
        self.assertEqual(report.matched, [])

    def test_same_title_different_posted_date_is_not_a_match(self):
        local = [
            Entry(title="Same title", posted=datetime(2020, 1, 1, tzinfo=timezone.utc))
        ]
        dump = [
            Entry(title="Same title", posted=datetime(2021, 1, 1, tzinfo=timezone.utc))
        ]

        report = diff_entries(local, dump)

        self.assertEqual(len(report.missing), 1)
        self.assertEqual(len(report.local_only), 1)
        self.assertEqual(report.matched, [])


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class ApplyMissingTest(TestCase):
    """Test copying missing entries (and their tags) into the local database."""

    def test_creates_entry_with_same_fields(self):
        posted = datetime(2020, 1, 1, tzinfo=timezone.utc)
        source = Entry.objects.create(
            created=posted,
            page=Entry.BLOG,
            title="Copied post",
            body="Some body text.",
            active=True,
            posted=posted,
        )

        warnings = apply_missing([source])

        self.assertEqual(warnings, [])
        copied = Entry.objects.exclude(pk=source.pk).get(title="Copied post")
        self.assertNotEqual(copied.pk, source.pk)
        self.assertEqual(copied.body, "Some body text.")
        self.assertEqual(copied.active, True)
        self.assertEqual(copied.posted, posted)

    def test_copies_tags_by_name(self):
        posted = datetime(2020, 1, 1, tzinfo=timezone.utc)
        source = Entry.objects.create(
            created=posted,
            page=Entry.BLOG,
            title="Tagged post",
            body="Body",
            posted=posted,
        )
        source.tags.add(Tag.objects.create(tag="django"))

        apply_missing([source])

        copied = Entry.objects.exclude(pk=source.pk).get(title="Tagged post")
        self.assertEqual([t.tag for t in copied.tags.all()], ["django"])

    def test_warns_about_images_without_copying_them(self):
        posted = datetime(2020, 1, 1, tzinfo=timezone.utc)
        source = Entry.objects.create(
            created=posted,
            page=Entry.BLOG,
            title="Post with image",
            body="Body",
            posted=posted,
        )
        source.images.add(
            Image.objects.create(
                image=SimpleUploadedFile(
                    "pixel.png", ONE_PIXEL_PNG, content_type="image/png"
                ),
                description="A single pixel.",
            )
        )

        warnings = apply_missing([source])

        self.assertEqual(len(warnings), 1)
        self.assertIn("Post with image", warnings[0])
        self.assertIn("1 image", warnings[0])
        copied = Entry.objects.exclude(pk=source.pk).get(title="Post with image")
        self.assertEqual(copied.images.count(), 0)

    def test_warns_about_comments_without_copying_them(self):
        posted = datetime(2020, 1, 1, tzinfo=timezone.utc)
        source = Entry.objects.create(
            created=posted,
            page=Entry.BLOG,
            title="Post with comment",
            body="Body",
            posted=posted,
        )
        Comment.objects.create(created=posted, body="Nice post!", entry=source)

        warnings = apply_missing([source])

        self.assertEqual(len(warnings), 1)
        self.assertIn("Post with comment", warnings[0])
        self.assertIn("1 comment", warnings[0])
        copied = Entry.objects.exclude(pk=source.pk).get(title="Post with comment")
        self.assertEqual(copied.comment_set.count(), 0)
