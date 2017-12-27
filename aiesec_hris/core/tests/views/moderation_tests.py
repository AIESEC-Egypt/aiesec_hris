import string
import random

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from ...factories import ProfileFactory, UserFactory, LCFactory, PositionFactory
from ...models import ResetPasswordCode


class AccountModerationTest(TestCase):
    def setUp(self):
        self.user = User(username="Amr")
        self.user.set_password("password")
        self.user.is_staff = True
        self.user.save()
        LCFactory()
        PositionFactory()
        self.profile = ProfileFactory(phone=11111, verification_issue=1)
        self.profile.user.set_password("password")
        self.profile.user.save()

    def test_moderation_view(self):
        res = self.client.get(reverse("moderation-list"))
        # will redirect to django administration login
        self.assertEqual(res.status_code, 302)
        self.client.login(username='Amr', password='password')
        res = self.client.get(reverse("moderation-list"))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.profile.phone)
        res = self.client.get("%s?search=%s" % (reverse("moderation-list"), self.user.first_name))
        self.assertEqual(res.status_code, 200)

    def test_active_url(self):
        self.client.login(username='Amr', password='password')
        self.assertEqual(self.profile.verification_issue, 1)
        testing_accept_url = "%s?testing=1" % self.profile.get_accept_url()
        self.client.get(testing_accept_url)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.verification_issue, 4)

    def test_decline_url(self):
        self.client.login(username='Amr', password='password')
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.verification_issue, 1)
        data = {
            'verification_issue': 2,
            'verification_issue_extra': "TESt",
        }
        res = self.client.post("%s?testing=1" % self.profile.get_decline_url(), data=data)
        self.assertEqual(res.status_code, 302)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.verification_issue, 2)

    def test_login_profile(self):
        data = {
            'username': self.profile.user.username,
            'password': "password"
        }
        res = self.client.post(reverse("login"), data=data)
        self.assertEqual(res.status_code, 401)
        self.profile.verification_issue = 4
        self.profile.save()
        self.profile.refresh_from_db()
        res = self.client.post(reverse("login"), data=data)
        self.assertEqual(res.status_code, 200)
        self.assertIn('_auth_user_id', self.client.session)

    def test_login_decline_account(self):
        data = {
            'username': self.profile.user.username,
            'password': "password"
        }
        self.profile.verification_issue = 2
        self.profile.save()
        self.profile.refresh_from_db()
        res = self.client.post(reverse('login'), data=data)
        self.assertEqual(res.status_code, 200)

    def test_update_profile_decline(self):
        self.profile.verification_issue = 2
        self.profile.save()
        self.profile.refresh_from_db()
        code_obj = ResetPasswordCode(user=self.profile.user)
        code_obj.save()
        res = self.client.get(reverse('profile-update',
                                      kwargs={'code': code_obj.code}))
        self.assertEqual(res.status_code, 200)

    def test_decline_update_profile(self):
        self.profile.verification_issue = 2
        self.profile.save()
        self.profile.refresh_from_db()
        code_obj = ResetPasswordCode(user=self.profile.user)
        code_obj.save()
        profile_update_url = reverse('profile-update',
                                     kwargs={'code': code_obj.code})
        res = self.client.get(profile_update_url)
        self.assertEqual(res.status_code, 200)
        fake_code = ''.join(
            random.SystemRandom().choice(
                string.ascii_uppercase + string.digits) for _ in range(32))
        profile_update_url = reverse('profile-update',
                                     kwargs={'code': fake_code})
        res = self.client.get(profile_update_url)
        self.assertEqual(res.status_code, 404)
