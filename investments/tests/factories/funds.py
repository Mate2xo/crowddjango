import factory

from investments.models import Fund

class FundFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Fund

    name = factory.Faker('sentence')
