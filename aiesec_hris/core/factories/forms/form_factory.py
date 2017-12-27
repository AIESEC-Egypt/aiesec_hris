import factory
from ...models import Form
from ..user_factory import UserFactory


class FormFactory(factory.DjangoModelFactory):
    class Meta:
        model = Form

    owner = factory.SubFactory(UserFactory)
    title = factory.Faker("text")
    external = False

    @factory.post_generation
    def share(self, create, extracted, **kwargs):
        if extracted:
            for user in extracted:
                self.share.add(user)
