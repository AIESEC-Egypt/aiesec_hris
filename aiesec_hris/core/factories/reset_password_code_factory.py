from django.contrib.auth.models import User

import factory
import factory.fuzzy

from ..models import ResetPasswordCode


class ResetPasswordCodeFactory(factory.DjangoModelFactory):
    class Meta:
        model = ResetPasswordCode

    user = factory.Iterator(User.objects.all())
