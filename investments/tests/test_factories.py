from django.test import TestCase
import pytest

from investments.models import Subscription
from investments.tests.factories.funds import FundFactory
from investments.tests.factories.subscriptions import SubscriptionFactory


def test_base_fund_is_valid():
    fund = FundFactory.build()
    assert fund.clean_fields() is None

# TODO: try to iterate on traits
def test_closable_fund_is_valid():
    fund = FundFactory.build(closable=True)
    assert fund.clean_fields() is None

def test_closed_fund_is_valid():
    fund = FundFactory.build(closed=True)
    assert fund.clean_fields() is None

def test_publishable_fund_is_valid():
    fund = FundFactory.build(publishable=True)
    assert fund.clean_fields() is None

def test_published_fund_is_valid():
    fund = FundFactory.build(published=True)
    assert fund.clean_fields() is None


@pytest.mark.django_db
def test_base_subscrption_is_valid():
    subscription: Subscription = SubscriptionFactory()

    assert subscription.full_clean() is None
