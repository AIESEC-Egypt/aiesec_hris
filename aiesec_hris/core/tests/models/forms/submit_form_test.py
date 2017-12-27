from django.test import TestCase
from ....factories import (UserFactory,
                           FormFactory,
                           SubmitFormFactory,
                           QuestionFactory,
                           AnswerFactory)


class SubmitFormTest(TestCase):
    def setUp(self):
        self.user = UserFactory(username="TESTER")
        self.form = FormFactory(owner=self.user)
        question = QuestionFactory(form=self.form)
        self.answer = AnswerFactory(question=question)
        self.submit_form = SubmitFormFactory(user=self.user,
                                             form=self.form)
        self.submit_form_visitor = SubmitFormFactory(user=None,
                                                     form=self.form)

    def test_submit_form_rep(self):
        self.assertEqual(self.submit_form.__str__(), "user:%s %s"
                         % (self.submit_form.user,
                            self.form,))

    def test_answers_factory(self):
        answer = AnswerFactory()
        submit_form = SubmitFormFactory(answers=(answer,))
        self.assertEqual(submit_form.answers.all().count(), 1)
