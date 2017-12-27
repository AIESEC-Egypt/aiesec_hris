import factory
import factory.fuzzy

from ..models import LC


class LCFactory(factory.DjangoModelFactory):
    class Meta:
        model = LC

    title = factory.Iterator([
        'GUC',
        'AUC',
        'MSA',
        'AAST CAIRO',
        'AAST ALEX',
        'MUST'])
