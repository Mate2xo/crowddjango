from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from accounts.tests.factories.users import UserFactory
from accounts.tests.factories.profiles import NaturalFactory

class ProfileDetailTests(TestCase):
    def test_required_login(self):
        response = self.client.get(reverse('accounts:profile_show'))

        self.assertIn('/accounts/login', response.url)

    def test_http_ok_status(self):
        user = UserFactory()
        NaturalFactory(user=user)

        self.client.login(username=user.username, password='passpass')
        response = self.client.get(reverse('accounts:profile_show'))

        self.assertEqual(response.status_code, 200)
