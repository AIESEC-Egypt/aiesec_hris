from django.test import TestCase
from ....factories import (
    QuestionFactory,
    AnswerFactory,
    FormFactory,
    UserFactory)
from ....models import Answer


class AnswerModelTest(TestCase):
    def setUp(self):
        UserFactory()
        FormFactory()
        QuestionFactory()
        self.answer = AnswerFactory()

    def test_answer_representation(self):
        visitor_answer = AnswerFactory()
        self.assertEqual(
            visitor_answer.__str__(),
            "%s: %s" % (
                visitor_answer.question,
                visitor_answer.value,))
