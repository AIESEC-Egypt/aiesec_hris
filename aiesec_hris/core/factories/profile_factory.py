import factory
import factory.fuzzy

from .user_factory import UserFactory
from ..models import Profile, LC, Position


class ProfileFactory(factory.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)
    lc = factory.Iterator(LC.objects.all())
    position = factory.Iterator(Position.objects.all())
    job_description = factory.Faker('text')
    address = factory.Faker('address')
    phone = factory.Faker('phone_number')
    photo = factory.django.ImageField(color='blue')
    expa_id = factory.fuzzy.FuzzyInteger(00000, 99999)
    national_id_number = factory.fuzzy.FuzzyInteger(00000000, 99999999)
    national_id_picture = factory.django.ImageField(color='blue')
    verification_issue = factory.fuzzy.FuzzyInteger(1, 4)

    gender = factory.fuzzy.FuzzyInteger(1, 2)
    date_of_birth = factory.Faker('date')
    has_ixp = factory.Iterator([True, False])
