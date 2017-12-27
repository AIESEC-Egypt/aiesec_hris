from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from ...models import ResetPasswordCode
from ...factories import ResetPasswordCodeFactory, ProfileFactory


class AuthenticationViewsTests(TestCase):
    def setUp(self):
        password = 'password'
        user = User(username='nader', email='alexan.nader@gmail.com')
        user.set_password(password)
        user.save()
        self.user = user
        self.password = password
        ProfileFactory(user=user)


    def test_login_render(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

        self.client.login(username=self.user.username, password='password')
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 302)

    def test_login_success(self):
        response = self.client.post(reverse('login'), data={
            'username': self.user.username, 'password': self.password})
        self.assertEqual(response.status_code, 200)

    def test_login_unsuccessful(self):
        response = self.client.post(reverse('login'), data={
            'username': self.user.username, 'password': 'wrong_password'})
        self.assertEqual(response.status_code, 401)

        response = self.client.post(reverse('login'), data={
            'username': 'wrong_nader', 'password': self.password})
        self.assertEqual(response.status_code, 401)

    def test_logout(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user.username, password=self.password)
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_change_password_render(self):
        self.client.login(username=self.user.username, password=self.password)

        response = self.client.get(reverse('change-password'))
        self.assertEqual(response.status_code, 200)

    def test_change_password_success(self):
        self.client.login(username=self.user.username, password=self.password)

        data = {
            'current_password': self.password,
            'new_password': 'new password',
            'new_password_2': 'new password'}
        response = self.client.post(reverse('change-password'), data=data)
        self.assertEqual(response.status_code, 200)

    def test_change_password_unsuccessful(self):
        self.client.login(username=self.user.username, password=self.password)

        data = {
            'current_password': 'wrong password',
            'new_password': 'new password',
            'new_password_2': 'new password'}
        response = self.client.post(reverse('change-password'), data=data)
        self.assertEqual(response.status_code, 400)

        data = {
            'current_password': self.password,
            'new_password': 'new password',
            'new_password_2': 'different password'}
        response = self.client.post(reverse('change-password'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_forgot_password_render(self):
        response = self.client.get(reverse('forgot-password'))
        self.assertEqual(response.status_code, 200)

    def test_forgot_password_successful(self):
        data = {
            'email': self.user.email
        }
        response = self.client.post(
            reverse('forgot-password') + '?testing=1', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ResetPasswordCode.objects.filter(user=self.user))

    def test_forgot_password_unsuccessful(self):
        data = {
            'email': 'non_existant_email@gmail.com'
        }
        response = self.client.post(
            reverse('forgot-password') + '?testing=1', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(ResetPasswordCode.objects.filter(user=self.user))

    def test_reset_password_render(self):
        rc = ResetPasswordCodeFactory(user=self.user)
        response = self.client.get(reverse(
            'reset-password', kwargs={'code': rc.code}))
        self.assertEqual(response.status_code, 200)

    def test_reset_password_successful(self):
        rc = ResetPasswordCodeFactory(user=self.user)
        password = 'hello world'
        data = {
            'new_password': password
        }
        response = self.client.post(reverse(
            'reset-password', kwargs={'code': rc.code}), data=data)
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(pk=self.user.pk)
        self.assertTrue(user.check_password(password))
