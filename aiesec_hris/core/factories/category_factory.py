import factory
import factory.fuzzy

from ..models import Category


class CategoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = Category

    title = factory.Iterator([
        'Leadership',
        'Awesomeness',
        'Social Science',
        'Ducks',
        'External Relations'])
