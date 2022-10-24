from django.contrib.auth.models import User
from django.test import TestCase

from investments.models import Fund, Subscription
from accounts.models import Legal, Natural

def create_subscription(username='patate', fundname='friteuse', companyname='Hocouteau no Ken'):
    user = User.objects.create_user(username=username, password='passpass')
    profile = Legal.objects.create(user=user, phone_number='007', name=companyname)
    fund = Fund.objects.create(name=fundname)
    return Subscription.objects.create(amount=1234, profile=profile, fund=fund)

class SubscriptionModelTests(TestCase):
    def test_subscription_display_is_the_legal_profile_name(self):
        subscription = create_subscription()

        self.assertEqual(repr(subscription), f'<Subscription: {subscription.profile.name}>')
