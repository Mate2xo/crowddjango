import factory
from datetime import date, timedelta

from investments.models import Fund


class FundFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Fund

    name = factory.Faker('sentence')

    class Params:
        publishable = factory.Trait(
            closing_date=(date.today() + timedelta(days=365)),
            goal=100000
        )
        published = factory.Trait(publishable=True, status=Fund.Status.PUBLISHED)
        closable = factory.Trait(
            published=True,
            closing_date=(date.today() - timedelta(days=1))
        )
        closed = factory.Trait(closable=True, status=Fund.Status.CLOSED)
