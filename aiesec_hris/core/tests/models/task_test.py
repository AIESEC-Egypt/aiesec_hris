from django.test import TestCase

from ...factories import TaskFactory, UserFactory


class TaskTest(TestCase):
    """
    Test cases for the model Task
    """
    def setUp(self):
        UserFactory.create_batch(4)
        self.task = TaskFactory()

    def test_string_representation(self):
        """
        Testing string representation
        Author: Nader Alexan
        """
        self.assertEqual(self.task.__str__(), '%s to %s: %s' % (
            self.task.assigner.get_full_name(),
            self.task.assignee.get_full_name(),
            self.task.title))
