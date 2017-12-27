from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

import json

from ...models import Notification
from ...factories import NotificationFactory, TaskFactory
from ..helpers import compare_lists


class NotificationViewsTests(TestCase):
    def setUp(self):
        user = User(username='nader')
        user.set_password('password')
        user.save()
        self.user = user
        self.client.login(username=user.username, password='password')
        TaskFactory.create_batch(5)
        NotificationFactory(read=True)
        NotificationFactory.create_batch(30)

    def test_notification_list_render(self):
        notifications = Notification.objects.filter(receiver=self.user)
        read = list(notifications.filter(read=True))
        unread = list(notifications.filter(read=False))
        response = self.client.get(reverse('notification-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            compare_lists(
                response.context['read'], read, 'pk'))
        self.assertTrue(
            compare_lists(
                response.context['unread'], unread, 'pk'))
        self.assertFalse(
            Notification.objects.filter(receiver=self.user, read=False))

    def test_unread_notifications_count(self):
        notifications_count = Notification.objects.filter(
            read=False, receiver=self.user).count()
        response = self.client.get(reverse('notification-count'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(str(response.content.decode("utf-8")))['count']
        self.assertEqual(data, notifications_count)
