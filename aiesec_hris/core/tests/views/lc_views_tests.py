from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from ...models import LC
from ...factories import LCFactory, PositionFactory, ProfileFactory
from ..helpers import compare_lists, compare_object


class LCViewsTests(TestCase):
    def setUp(self):
        LCFactory.create_batch(5)
        PositionFactory.create_batch(5)

        mc_user = User(username='mc user')
        mc_user.set_password('password')
        mc_user.save()
        self.mc_user = mc_user
        self.mc_user = mc_user
        self.mc_profile = ProfileFactory(
            user=self.mc_user, position=PositionFactory(type=1))

        lc_user = User(username='lc user')
        lc_user.set_password('password')
        lc_user.save()
        self.lc_user = lc_user
        self.lc_profile = ProfileFactory(
            user=self.lc_user, position=PositionFactory(type=2))

        ProfileFactory.create_batch(10)

    def test_lc_list(self):
        self.client.login(username=self.mc_user.username, password='password')
        response = self.client.get(reverse('lc-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            compare_lists(
                response.context['object_list'],
                LC.objects.all(),
                'id'))

        self.client.login(username=self.lc_user.username, password='password')
        response = self.client.get(reverse('lc-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            compare_lists(
                response.context['object_list'],
                [self.lc_user.profile.lc],
                'id'))

    def test_lc_detail(self):
        lc = LC.objects.first()
        self.client.login(username=self.mc_user.username, password='password')
        response = self.client.get(reverse('lc-detail', kwargs={'pk': lc.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['object'],
            lc)
