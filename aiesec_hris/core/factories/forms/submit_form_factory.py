import factory
from ...models import Form, SubmitForm
from ..user_factory import UserFactory
from .form_factory import FormFactory


class SubmitFormFactory(factory.DjangoModelFactory):
    class Meta:
        model = SubmitForm

    form = factory.SubFactory(FormFactory)
    user = factory.SubFactory(UserFactory)

    @factory.post_generation
    def answers(self, create, extracted, **kwargs):
        if extracted:
            for answer in extracted:
                self.answers.add(answer)
