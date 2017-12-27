from django.test import TestCase

from ...factories import UserFactory, CategoryFactory


class CategoryTest(TestCase):

    def test_string_representation(self):
        UserFactory.create_batch(4)
        category = CategoryFactory()
        self.assertEqual(category.__str__(), category.title)
