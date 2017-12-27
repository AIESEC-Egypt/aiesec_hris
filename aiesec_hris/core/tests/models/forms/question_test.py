from django.test import TestCase
from ....factories import FormFactory, QuestionFactory


class QuestionModelTest(TestCase):
    def setUp(self):
        FormFactory()
        self.question = QuestionFactory()

    def test_question_representation(self):
        self.assertEqual(self.question.__str__(),
                         "%s: %s" % (self.question.form, self.question.question))