from django.contrib.auth.models import User
import factory
import factory.fuzzy

from ..models import Notification, Task


class NotificationFactory(factory.DjangoModelFactory):
    class Meta:
        model = Notification

    receiver = factory.Iterator(User.objects.all())
    text = factory.Faker('text')
    content_object = factory.Iterator(Task.objects.all())
    action = factory.Iterator([1, 3])
