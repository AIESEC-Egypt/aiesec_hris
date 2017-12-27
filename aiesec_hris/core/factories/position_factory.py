import factory
import factory.fuzzy

from ..models import Position, LC


class PositionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Position

    title = factory.Iterator([
        'P',
        'VP ER',
        'VP IM',
        'VP OGX',
        'VP ICX',
        'TL ER',
        'TL IM',
        'TL OGX',
        'TL ICX',
        'MEMBER ER',
        'MEMBER IM',
        'MEMBER OGX',
        'MEMBER ICX'])
    lc = factory.Iterator(LC.objects.all())
    type = factory.fuzzy.FuzzyInteger(1, 2)
    parent = factory.Iterator(
        [position for position in Position.objects.all()] + [None])
