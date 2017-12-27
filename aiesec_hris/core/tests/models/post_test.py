from django.test import TestCase

from ...factories import PostFactory, UserFactory


class PostTest(TestCase):

    def test_string_representation(self):
        UserFactory.create_batch(4)
        post = PostFactory()
        self.assertEqual(post.__str__(), post.title)
