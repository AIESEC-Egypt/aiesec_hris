from django.test import TestCase

from ...factories import EventFactory, UserFactory


class EventTest(TestCase):

    def test_string_representation(self):
        UserFactory.create_batch(4)
        event = EventFactory()
        self.assertEqual(event.__str__(), event.title)
