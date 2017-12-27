from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

import json

from ...models import Event, Notification
from ...factories import EventFactory, UserFactory
from ..helpers import compare_lists, compare_object


class EventsViewsTests(TestCase):
    def setUp(self):
        user = User(username='nader')
        user.set_password('password')
        user.save()
        self.user = user
        self.client.login(username=user.username, password='password')
        UserFactory.create_batch(5)
        EventFactory.create_batch(5)

    def test_event_list_render(self):
        response = self.client.get(reverse('event-list'))
        self.assertEqual(response.status_code, 200)

    def test_event_list(self):
        response = self.client.get(reverse('event-list-json'))
        self.assertEqual(response.status_code, 200)
        qs = Event.objects.all()
        data = json.loads(str(response.content.decode("utf-8")))['monthly']
        self.assertTrue(
            compare_lists(data, qs, 'id', first_list_is_dict=True))

    def test_event_create(self):
        invitees = User.objects.all().values_list('pk', flat=True)
        data = {
            'title': 'hello world',
            'notes': 'lorem impsum',
            'start_date': '2017-10-10',
            'start_time': '10:00',
            'end_date': '2017-10-10',
            'end_time': '15:00',
            'invitees': invitees
        }
        response = self.client.post(reverse('event-create'), data=data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            Event.objects.get(title='hello world', notes='lorem impsum'))
        for invitee in invitees:
            self.assertTrue(Notification.objects.filter(
                receiver__id=invitee, action=10))

    def test_event_update(self):
        event = self.user.events_created.first()
        data = {
            'pk': event.pk,
            'title': 'hello world NEW',
            'notes': 'lorem impsum NEW',
            'start_date': '2017-10-11',
            'end_date': '2017-10-11',
        }
        response = self.client.post(
            reverse('event-update', kwargs={'pk': event.pk}), data=data)
        self.assertEqual(response.status_code, 302)
        event = self.user.events_created.first()
        data.pop('start_date')
        data.pop('end_date')
        self.assertTrue(compare_object(data, event))

    def test_event_delete(self):
        pk = self.user.events_created.first().pk
        response = self.client.get(
            reverse('event-delete', kwargs={'pk': pk}))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Event.objects.filter(pk=pk))

    def test_event_detail(self):
        event = self.user.events_created.first()
        pk = event.pk
        response = self.client.get(
            reverse('event-detail', kwargs={'pk': pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'], event)
