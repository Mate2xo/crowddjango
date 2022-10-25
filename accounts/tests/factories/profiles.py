from django.contrib.contenttypes.models import ContentType
import factory

from accounts.models import Legal, Natural
from accounts.tests.factories.users import UserFactory

class NaturalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Natural

    user = factory.SubFactory(UserFactory)

    phone_number = factory.Faker('phone_number')
    place_of_birth = factory.Faker('city')

class LegalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Legal

    user = factory.SubFactory(UserFactory)

    legal_representative_first_name = factory.Faker('first_name')
    legal_representative_last_name = factory.Faker('last_name')
    name = 'Evil Corp ltd'
    phone_number = factory.Faker('phone_number')
