from django.test import TestCase

from investments.tests.factories.funds import FundFactory
from investments.tests.factories.subscriptions import SubscriptionFactory

class FactoryTests(TestCase):
    def test_base_fund_is_valid(self):
        fund = FundFactory.build()

        self.assertEqual(fund.full_clean(), None)

    def test_base_subscrption_is_valid(self):
        subscription = SubscriptionFactory()

        self.assertEqual(subscription.full_clean(), None)
