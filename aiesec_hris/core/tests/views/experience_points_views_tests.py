from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from ...factories import (
    ProfileFactory)
from ...models import ExperiencePoints


class ExperiencePointsViewsTest(TestCase):
    def setUp(self):
        self.user = User(username="anwar")
        self.user.set_password("password")
        self.user.save()
        ProfileFactory(user=self.user)

    def test_update_render(self):
        self.client.login(username=self.user.username, password='password')
        response = self.client.get(reverse(
            'experience-points-update',
            kwargs={'pk': self.user.experience_points.pk}))
        self.assertEqual(response.status_code, 200)

    def test_update(self):
        self.client.login(username=self.user.username, password='password')
        data = {'introduction': 'on'}
        response = self.client.post(
            reverse(
                'experience-points-update',
                kwargs={'pk': self.user.experience_points.pk}),
            data=data)
        self.assertEqual(response.status_code, 200)
        ep = ExperiencePoints.objects.get(pk=self.user.experience_points.pk)
        self.assertTrue(ep.introduction)
