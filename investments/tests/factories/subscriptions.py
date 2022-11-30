import factory

from accounts.tests.factories.profiles import LegalFactory
from investments.models import Subscription
from investments.tests.factories.funds import FundFactory


class SubscriptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Subscription

    fund = factory.SubFactory(FundFactory)
    profile = factory.SubFactory(LegalFactory)

    amount = 2000
