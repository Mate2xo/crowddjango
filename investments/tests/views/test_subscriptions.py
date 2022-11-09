from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext as _

from accounts.tests.factories.users import UserFactory
from investments.tests.factories.subscriptions import SubscriptionFactory


class SubscriptionListTests(TestCase):
    def test_index_requires_login(self):
        response = self.client.get(reverse('investments:dashboard'))

        self.assertIn('accounts/login', response.url)

    def test_index_only_shows_the_current_user_subscriptions(self):
        subscription1 = SubscriptionFactory()
        SubscriptionFactory()
        self.client.login(username=subscription1.profile.user.username, password='passpass')

        response = self.client.get(reverse('investments:dashboard'))

        self.assertQuerysetEqual(response.context['object_list'], [subscription1])

    def test_index_shows_message_when_there_are_no_subscriptions(self):
        user = UserFactory(with_natural_profile=True)
        self.client.login(username=user.username, password='passpass')

        response = self.client.get(reverse('investments:dashboard'))

        self.assertContains(response, _('You have not subscribed to any fund'))


class SubscriptionViewTests(TestCase):
    def test_show_requires_login(self):
        response = self.client.get(reverse('investments:subscription_detail', args=[999]))

        self.assertIn('accounts/login', response.url)

    def test_show_is_200_for_current_user_subscription(self):
        subscription = SubscriptionFactory()
        self.client.login(username=subscription.profile.user.username, password='passpass')

        response = self.client.get(reverse('investments:subscription_detail', args=[subscription.id]))

        self.assertEqual(response.status_code, 200)

    def test_show_is_404_for_other_user_subscription(self):
        other_user_subscription = SubscriptionFactory() # for another user
        current_user = UserFactory()
        self.client.login(username=current_user.username, password='passpass')

        response = self.client.get(reverse('investments:subscription_detail', args=[other_user_subscription.id]))

        self.assertEqual(response.status_code, 404)
