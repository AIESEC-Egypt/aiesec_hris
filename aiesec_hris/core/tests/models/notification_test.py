from django.test import TestCase

from ...factories import (
    NotificationFactory, UserFactory, TaskFactory)


class NotificationTest(TestCase):

    def test_string_representation(self):
        UserFactory()
        TaskFactory()
        notification = NotificationFactory()

        self.assertEqual(
            notification.__str__(), notification.text)
