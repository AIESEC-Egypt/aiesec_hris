from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from ...factories import (
    UserFactory,
    LCFactory,
    ProfileFactory,
    PositionFactory)
from ...models import Task, Notification
from ..helpers import compare_lists

import datetime


class StatsViewsTests(TestCase):
    def setUp(self):
        LCFactory.create_batch(5)
        PositionFactory.create_batch(5)
        position = PositionFactory(type=1)
        profile = ProfileFactory(position=position)
        self.user = profile.user
        self.password = 'password'
        self.user.set_password(self.password)
        self.user.save()
        self.client.login(username=self.user.username, password=self.password)
        ProfileFactory.create_batch(30)

    def test_stats_render(self):
        response = self.client.get(reverse('stats'))
        self.assertEqual(response.status_code, 200)
