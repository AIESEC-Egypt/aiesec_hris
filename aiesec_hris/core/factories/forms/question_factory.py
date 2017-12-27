import factory
import factory.fuzzy
from ...models import Form, Question


class QuestionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Question

    form = factory.Iterator(Form.objects.all())
    question = factory.Faker("text")
    required = False
    multiple = False
    type = factory.fuzzy.FuzzyInteger(1, 2)

