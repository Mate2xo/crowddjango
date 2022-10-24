from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext as _

from investments.models import Fund, Subscription
from accounts.models import Legal, Natural

def create_subscription(username='patate', fundname='friteuse', companyname='Hocouteau no Ken'):
    user = User.objects.create_user(username=username, password='passpass')
    profile = Legal.objects.create(user=user, phone_number='007', name=companyname)
    fund = Fund.objects.create(name=fundname)
    return Subscription.objects.create(amount=1234, profile=profile, fund=fund)

class SubscriptionListTests(TestCase):
    def test_index_requires_login(self):
        response = self.client.get(reverse('investments:dashboard'))

        self.assertIn('accounts/login', response.url)

    def test_index_only_shows_the_current_user_subscriptions(self):
        subscription1 = create_subscription()
        subscription2 = create_subscription(username='frite', fundname='au four')
        self.client.login(username=subscription1.profile.user, password='passpass')

        response = self.client.get(reverse('investments:dashboard'))

        self.assertQuerysetEqual(response.context['object_list'], [subscription1])

    def test_index_shows_message_when_there_are_no_subscriptions(self):
        user = User.objects.create_user(username='newbe', password='passpass')
        Legal.objects.create(user=user, phone_number='007', name='omae ha mou shindeiru')
        self.client.login(username=user.username, password='passpass')

        response = self.client.get(reverse('investments:dashboard'))

        self.assertContains(response, _('You have not subscribed to any fund'))

class SubscriptionViewTests(TestCase):
    def test_show_requires_login(self):
        response = self.client.get(reverse('investments:subscription_detail', args=[999]))

        self.assertIn('accounts/login', response.url)

    def test_show_is_200_for_current_user_subscription(self):
        subscription = create_subscription()
        self.client.login(username=subscription.profile.user, password='passpass')

        response = self.client.get(reverse('investments:subscription_detail', args=[subscription.id]))

        self.assertEqual(response.status_code, 200)

    def test_show_is_404_for_other_user_subscription(self):
        other_user_subscription = create_subscription() # for another user
        User.objects.create_user(username='current', password='passpass')
        self.client.login(username='current', password='passpass')

        response = self.client.get(reverse('investments:subscription_detail', args=[other_user_subscription.id]))

        self.assertEqual(response.status_code, 404)
