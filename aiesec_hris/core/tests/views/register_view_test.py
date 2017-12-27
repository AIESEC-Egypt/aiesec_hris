from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from ...factories import (
    LCFactory,
    PositionFactory,
    ProfileFactory)
from ...models import LC, Position


class RegisterViewTests(TestCase):
    def setUp(self):
        LCFactory.create_batch(5)
        PositionFactory.create_batch(5)

    def test_register_render(self):
        self.client.get(reverse('register'))

    def test_register_success(self):
        lc = LC.objects.first()
        position = Position.objects.filter(lc=lc).first()
        data = {
            'lc': lc.pk,
            'position': position.pk,
            'job_description': 'lorem impsum',
            'address': '50 Road 70, Maadi',
            'phone': '012002130213',
            'expa_id': '123213',
            'national_id_number': '123213921',
            'gender': 1,
            'date_of_birth': '12/02/1991'
        }
        self.client.post(reverse('register'), data=data)
