from django.test import TestCase

from ...factories import ResetPasswordCodeFactory, UserFactory


class ResetPasswordCodeTest(TestCase):

    def test_string_representation(self):
        UserFactory()
        rc = ResetPasswordCodeFactory()
        self.assertEqual(rc.__str__(), rc.user.username)
