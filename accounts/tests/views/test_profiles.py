from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from accounts.models import Profile

class ProfileDetailTests(TestCase):
    def test_required_login(self):
        response = self.client.get(reverse('accounts:profile_show'))

        self.assertIn('/accounts/login', response.url)

    def test_http_ok_status(self):
        user = User.objects.create_user(username='cookie', password='passpass')
        Profile.objects.create(user=user, phone_number='1234')

        self.client.login(username='cookie', password='passpass')
        response = self.client.get(reverse('accounts:profile_show'))

        self.assertEqual(response.status_code, 200)
