from django.test import TestCase
from ...factories import (
    LCFactory,
    PositionFactory,
    ProfileFactory)


class ProfileTest(TestCase):

    def setUp(self):
        LCFactory()
        PositionFactory()
        self.profile = ProfileFactory()

    def test_string_representation(self):
        self.assertEqual(
            self.profile.__str__(), '%s %s' % (
                self.profile.user.first_name, self.profile.user.last_name))

    def test_deletion(self):
        self.profile.delete()
