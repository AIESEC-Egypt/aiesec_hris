from django.test import TestCase
from django.utils import timezone
from ....factories import FormFactory, UserFactory
from ....models import Form


class FormModelTest(TestCase):
    def setUp(self):
        user = UserFactory()
        self.form = FormFactory(share=(user,))
        self.my_form = Form(title="TEST")

    def test_form_representation(self):
        self.assertEqual(str(self.my_form), "TEST")
        self.assertEqual(self.form.__str__(), self.form.title)
        self.assertLess(self.form.created_at, timezone.now())