from django.contrib.auth.models import User
import factory
import factory.fuzzy

from ..models import Event


class EventFactory(factory.DjangoModelFactory):
    class Meta:
        model = Event

    owner = factory.Iterator(User.objects.all())

    title = factory.Faker('text')
    notes = factory.Faker('text')
    location = factory.Faker('address')
    start_date = factory.Faker('date')
    start_time = factory.Faker('time')
    end_date = factory.Faker('date')
    end_time = factory.Faker('time')
