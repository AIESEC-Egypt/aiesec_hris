import factory
from django.contrib.auth.models import User


def generate_username():
    i = 1
    while User.objects.filter(username='user_%d' % i):
        i += 1
    return 'user_%d' % i


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User
    username = factory.LazyFunction(generate_username)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.LazyAttribute(lambda a:
                                  '{0}.{1}@example.com'.format(a.first_name,
                                                               a.last_name).lower())
    is_staff = False
    is_superuser = False
