from django.contrib.auth.models import User

import factory
import factory.fuzzy
import datetime

from ..models import Task


class TaskFactory(factory.DjangoModelFactory):
    class Meta:
        model = Task

    assigner = factory.Iterator(User.objects.all())
    assignee = factory.Iterator(User.objects.all())

    title = factory.Faker('text')
    description = factory.Faker('text')
    status = factory.fuzzy.FuzzyInteger(1, 4)
    submission_type = factory.fuzzy.FuzzyInteger(1, 2)
    submission = factory.Faker('text')
    deadline = factory.Iterator([
        datetime.datetime.now() - datetime.timedelta(days=2),
        datetime.datetime.now(),
        datetime.datetime.now() + datetime.timedelta(days=2)])
