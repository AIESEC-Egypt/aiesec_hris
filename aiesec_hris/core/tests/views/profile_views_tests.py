from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from ...models import Profile
from ...factories import LCFactory, PositionFactory, ProfileFactory


class ProfileViewsTests(TestCase):
    def setUp(self):
        LCFactory.create_batch(5)
        PositionFactory.create_batch(5)

        self.mc_password = 'password'
        mc_user = User(username='mc user')
        mc_user.set_password(self.mc_password)
        mc_user.save()
        self.mc_user = mc_user
        self.mc_user = mc_user
        self.mc_profile = ProfileFactory(
            user=self.mc_user, position=PositionFactory(type=1))
        self.client.login(username=self.mc_user.username, password='password')

    def test_profile_detail(self):
        profile = ProfileFactory()
        response = self.client.get(
            profile.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'], profile)

    def test_update_profile_render(self):
        self.client.login(
            username=self.mc_user.username,
            password=self.mc_password)

        response = self.client.get(reverse(
            'profile-update', kwargs={'pk': self.mc_user.profile.pk}))
        self.assertEqual(response.status_code, 200)

    def test_update_profile_successful(self):
        self.client.login(
            username=self.mc_user.username, password=self.mc_password)

        data = {
            'lc': self.mc_profile.lc.pk,
            'position': self.mc_profile.position.pk,
            'job_description': self.mc_profile.job_description,
            'address': self.mc_profile.address,
            'phone': self.mc_profile.phone,
            'photo': self.mc_profile.photo,
            'national_id_number': self.mc_profile.national_id_number,
            'national_id_picture': self.mc_profile.national_id_picture,
            'expa_id': '1234',
            'gender': self.mc_profile.gender,
            'date_of_birth': self.mc_profile.date_of_birth,
            'has_ixp': self.mc_profile.has_ixp,
        }
        response = self.client.post(
            reverse(
                'profile-update', kwargs={'pk': self.mc_user.profile.pk}
            ),
            data=data)
        self.assertEqual(response.status_code, 200)
        profile = Profile.objects.get(pk=self.mc_user.profile.pk)
        self.assertEqual(profile.expa_id, data.get('expa_id'))
