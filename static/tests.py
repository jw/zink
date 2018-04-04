from django.test import TransactionTestCase

from static.models import Static


class StaticsTestCase(TransactionTestCase):

    def test_animals_can_speak(self):
        """Ensure that the default assets are there"""
        rero = Static.objects.get(name="copyright").value
        copyright = Static.objects.get(name="copyright").value,
        title = Static.objects.get(name="title").value
        self.assertEqual(title, 'ElevenBits')
