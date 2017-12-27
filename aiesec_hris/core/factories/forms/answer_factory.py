import factory
import factory.fuzzy
from ...models import Question, Answer
from ..user_factory import UserFactory
from django.contrib.auth.models import User


class AnswerFactory(factory.DjangoModelFactory):
    class Meta:
        model = Answer

    question = factory.Iterator(Question.objects.all())
    value = factory.Faker("text")
