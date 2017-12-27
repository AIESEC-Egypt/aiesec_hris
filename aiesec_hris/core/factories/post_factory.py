# Avoid importing settings directly to
# allow tests to use test-specific settings
from django.conf import settings
from django.contrib.auth.models import User
import factory
import factory.fuzzy

from ..models import Post, Category


class PostFactory(factory.DjangoModelFactory):
    class Meta:
        model = Post

    category = factory.Iterator(Category.objects.all())
    editor = factory.Iterator(User.objects.all())

    title = factory.Faker('text')

    @factory.post_generation
    def category(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of categories were passed in, use them
            for category in extracted:
                self.category.add(category)
        else:
            for category in Category.objects.all():
                self.category.add(category)
