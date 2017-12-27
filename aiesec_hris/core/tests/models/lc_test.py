from django.test import TestCase

from ...models import LC


class LCTest(TestCase):

    def test_string_representation(self):
        lc = LC(title="GUC")
        lc.save()
        self.assertEqual(lc.__str__(), lc.title)
