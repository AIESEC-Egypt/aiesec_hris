import factory.fuzzy

from aiesec_hris.education.models import Category


class CategoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = Category

    title = factory.Iterator([
        'Leadership',
        'Awesomeness',
        'Social Science',
        'Ducks',
        'External Relations'])
