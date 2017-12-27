from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from ...factories import UserFactory, TaskFactory
from ...models import Task, Notification
from ..helpers import compare_lists

import datetime


class TaskViewsTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.password = 'password'
        self.user.set_password(self.password)
        self.user.save()
        self.client.login(username=self.user.username, password=self.password)
        UserFactory.create_batch(3)

        TaskFactory(assigner=self.user)
        TaskFactory(assignee=self.user, status=1)
        TaskFactory(assignee=self.user, status=2)
        TaskFactory(assignee=self.user, status=3)

    def test_task_list_render(self):
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, 200)

        qs = Task.objects.filter(assignee=self.user, status=1)
        self.assertTrue(compare_lists(response.context['new_tasks'], qs, 'id'))

        qs = Task.objects.filter(assignee=self.user, status=2)
        self.assertTrue(
            compare_lists(response.context['submitted_tasks'], qs, 'id'))

        qs = Task.objects.filter(assignee=self.user, status=3)
        self.assertTrue(
            compare_lists(response.context['accepted_tasks'], qs, 'id'))

        qs = Task.objects.filter(assigner=self.user,)
        self.assertTrue(
            compare_lists(response.context['created_by_me_tasks'], qs, 'id'))

    def test_task_create_successful(self):
        title = 'hello world'
        description = 'lorem impsum'
        deadline = datetime.datetime.today() + datetime.timedelta(days=2)
        deadline = deadline.date()
        data = {
            'title': title,
            'description': description,
            'submission_type': 1,
            'deadline': deadline,
            'assignee': User.objects.exclude(pk=self.user.pk).first().pk}
        response = self.client.post(reverse('task-create'), data=data)
        self.assertEqual(response.status_code, 201)
        task = Task.objects.get(title=title, assigner=self.user)
        self.assertEqual(task.description, description)
        self.assertEqual(task.submission_type, 1)
        self.assertEqual(task.deadline, deadline)

        self.assertTrue(Notification.objects.filter(
            receiver=task.assignee, task=task, action=1).exists())

    def test_task_detail_render(self):
        task = self.user.assignee.first()
        response = self.client.get(
            reverse('task-detail', kwargs={'pk': task.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'].pk, task.pk)

    def test_task_detail_unsuccessful(self):
        task = TaskFactory(assignee=UserFactory(), assigner=UserFactory())
        response = self.client.get(
            reverse('task-detail', kwargs={'pk': task.pk}))
        self.assertEqual(response.status_code, 404)

    def test_task_status_update_successful(self):
        task = self.user.assigner.first()
        task.status = 2
        task.save()
        pk = task.pk

        response = self.client.get(
            reverse(
                'task-status-update',
                kwargs={'pk': pk, 'status': 'accept'}))
        self.assertEqual(response.status_code, 302)

        task = Task.objects.get(pk=pk)
        self.assertEqual(task.status, 3)

        self.assertTrue(Notification.objects.filter(
            receiver=task.assignee, task=task, action=2).exists())
        Notification.objects.all().delete()

        response = self.client.get(
            reverse(
                'task-status-update',
                kwargs={'pk': pk, 'status': 'reject'}))
        self.assertEqual(response.status_code, 302)

        self.assertTrue(Notification.objects.filter(
            receiver=task.assignee, task=task, action=2).exists())

        task = Task.objects.get(pk=pk)
        self.assertEqual(task.status, 4)

    def test_task_status_update_unsuccessful(self):
        task = self.user.assigner.first()
        pk = task.pk
        initial_status = task.status
        response = self.client.get(
            reverse(
                'task-status-update',
                kwargs={'pk': pk, 'status': 'hi'}))
        self.assertEqual(response.status_code, 302)

        self.assertFalse(Notification.objects.filter(
            receiver=task.assigner, task=task, action=2).exists())

        task = Task.objects.get(pk=pk)
        self.assertEqual(task.status, initial_status)

        task.assigner = User.objects.exclude(pk=self.user.pk).first()
        task.save()
        response = self.client.get(
            reverse(
                'task-status-update',
                kwargs={'pk': pk, 'status': 'accept'}))
        self.assertEqual(response.status_code, 404)

        self.assertFalse(Notification.objects.filter(
            receiver=task.assignee, task=task, action=2).exists())

    def test_task_submit_successful(self):
        task = self.user.assignee.first()
        task.status = 1
        task.save()
        pk = task.pk
        submission = 'hello world'
        response = self.client.post(
            reverse(
                'task-submit',
                kwargs={'pk': pk}),
            data={'submission': submission})
        self.assertEqual(response.status_code, 302)

        task = Task.objects.get(pk=pk)
        self.assertEqual(task.submission, submission)
        self.assertEqual(task.status, 2)

        self.assertTrue(Notification.objects.filter(
            receiver=task.assigner, task=task, action=3).exists())

    def test_task_submit_unsuccessful(self):
        task = TaskFactory(assignee=UserFactory(), assigner=UserFactory())
        pk = task.pk
        submission = 'hello world'
        initial_submission = task.submission
        initial_status = task.status
        response = self.client.post(
            reverse(
                'task-submit',
                kwargs={'pk': pk}),
            data={'submission': submission})
        self.assertEqual(response.status_code, 404)

        task = Task.objects.get(pk=pk)
        self.assertEqual(task.submission, initial_submission)
        self.assertEqual(task.status, initial_status)
        self.assertFalse(Notification.objects.filter(
            receiver=task.assigner, task=task, action=3).exists())

    def test_task_delete_successful(self):
        task = TaskFactory(assignee=UserFactory(), assigner=self.user)
        pk = task.pk
        response = self.client.post(
            reverse(
                'task-delete',
                kwargs={'pk': pk}))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.filter(pk=pk))

    def test_task_delete_unsuccessful(self):
        task = TaskFactory(assignee=self.user, assigner=UserFactory())
        pk = task.pk
        response = self.client.post(
            reverse(
                'task-delete',
                kwargs={'pk': pk}))
        self.assertEqual(response.status_code, 401)
        self.assertTrue(Task.objects.filter(pk=pk))
