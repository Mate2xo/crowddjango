from django.test import TestCase

from investments.tests.factories.subscriptions import SubscriptionFactory

class SubscriptionModelTests(TestCase):
    def test_subscription_display_is_the_legal_profile_name(self):
        subscription = SubscriptionFactory()

        self.assertEqual(repr(subscription), f'<Subscription: {subscription.profile.name}>')
