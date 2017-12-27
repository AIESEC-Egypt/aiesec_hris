from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from ...models import Form, SubmitForm
from ...factories import (
    FormFactory,
    SubmitFormFactory,
    QuestionFactory,
    AnswerFactory)


class FormViewTest(TestCase):
    def setUp(self):
        self.user = User(username="anwar")
        self.user.set_password("password")
        self.user.save()
        self.tester = User(username="tester")
        self.tester.set_password("password")
        self.tester.save()
        self.form = FormFactory(owner=self.user)

    def test_forms_views(self):
        res = self.client.get(reverse('form-list'))
        self.assertEqual(res.status_code, 302)

        self.client.login(username='anwar', password='password')
        res = self.client.get(reverse('form-list'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.form.title)

    def test_forms_detail(self):
        self.client.login(username='anwar', password='password')
        res = self.client.get(self.form.get_absolute_url())
        self.assertEqual(res.status_code, 200)

    def test_form_delete(self):
        self.client.login(username=self.user.username, password='password')
        form = self.user.form_owner.first()
        response = self.client.get(
            reverse('form-delete', kwargs={'pk': form.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Form.objects.filter(pk=form.pk))

    def test_form_create(self):
        self.client.login(username=self.user.username, password='password')
        data = {
            "question-0-type": "2",
            "question-0-choices": "",
            "question-0-question": "hello w?",
            "num_questions": "1",
            "title": "hello world",
            "question-MAX_NUM_FORMS": "1000",
            "question-TOTAL_FORMS": "1",
            "question-INITIAL_FORMS": "0",
            "question-0-required": "on",
            "share": self.user.pk,
            "question-MIN_NUM_FORMS": "0",
        }
        response = self.client.post(
            reverse('form-create'), data=data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Form.objects.filter(title=data['title']))

    def test_submission_detail_render(self):
        self.client.login(username=self.user.username, password='password')
        submission = SubmitFormFactory(
            user=self.user,
            form=self.form)
        AnswerFactory()
        response = self.client.get(
            reverse('submission-detail', kwargs={'pk': submission.pk}))
        self.assertEqual(response.status_code, 200)

    def test_submission_create_visitor(self):
        form = FormFactory(external=True)
        response = self.client.get(
            reverse('submission-login', kwargs={'pk': form.pk}))
        self.assertEqual(response.status_code, 200)

        data = {'visitor_email': 'alexan.nader@gmail.com'}
        response = self.client.post(
            reverse('submission-login', kwargs={'pk': form.pk}), data=data)
        self.assertEqual(response.status_code, 200)

        submit_form = SubmitForm.objects.get(
            visitor_email=data['visitor_email'])

        response = self.client.get(
            reverse(
                'submission-create',
                kwargs={'pk': form.pk, 'submit_form_pk': submit_form.pk}))
        self.assertEqual(response.status_code, 200)

        data = {}
        for i, question in enumerate(form.question_form.all()):
            data['answer-%d-value' % i] = '1'
        response = self.client.post(
            reverse(
                'submission-create',
                kwargs={'pk': form.pk, 'submit_form_pk': submit_form.pk}),
            data=data)
        self.assertEqual(response.status_code, 200)

    def test_submission_create_user(self):
        self.client.login(username=self.user.username, password='password')
        form = FormFactory(external=True)
        response = self.client.get(
            reverse('submission-login', kwargs={'pk': form.pk}))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(
            reverse(
                'submission-create',
                kwargs={'pk': form.pk}))
        self.assertEqual(response.status_code, 200)

        data = {}
        for i, question in enumerate(form.question_form.all()):
            data['answer-%d-value' % i] = '1'
        response = self.client.post(
            reverse(
                'submission-create',
                kwargs={'pk': form.pk}),
            data=data)
        self.assertEqual(response.status_code, 200)
