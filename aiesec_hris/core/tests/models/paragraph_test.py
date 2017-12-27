from django.test import TestCase

from ...factories import (
    UserFactory,
    PostFactory,
    ParagraphFactory)


class ParagraphTest(TestCase):

    def setUp(self):
        UserFactory()
        PostFactory()
        self.paragraph = ParagraphFactory()

    def test_string_representation(self):
        self.assertEqual(
            self.paragraph.__str__(), '%s: %s' % (
                self.paragraph.post.title, self.paragraph.text))
