import factory
import pytest

from investments.models import Subscription
from investments.tests.factories.funds import FundFactory
from investments.tests.factories.subscriptions import SubscriptionFactory


def test_base_fund_is_valid():
    fund = FundFactory.build()
    assert fund.clean_fields() is None


fund_params = FundFactory.__dict__['_meta'].parameters
fund_traits = {key: value for key, value in fund_params.items() if type(value) == factory.declarations.Trait}


@pytest.mark.parametrize('trait', fund_traits.keys())
@pytest.mark.django_db
def test_fund_traits_are_valid(trait):
    fund = FundFactory.build(**{trait: True})
    assert fund.full_clean() is None


@pytest.mark.django_db
def test_base_subscrption_is_valid():
    subscription: Subscription = SubscriptionFactory()

    assert subscription.full_clean() is None
