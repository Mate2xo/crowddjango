from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from accounts.models import Profile

class SignUpGet(TestCase):
    def test_http_ok_status(self):
        response = self.client.get(reverse('accounts:signup'))

        self.assertEqual(response.status_code, 200)

class SignUpPost(TestCase):
    def test_with_valid_arguments_associates_user_with_profile(self):
        params = {
            'username': 'polo_et_pan',
            'first_name': 'polo',
            'last_name': 'pan',
            'password1': 'P@assword1',
            'password2': 'P@assword1',
            'profile_type': 'Natural'
        }

        self.client.post('/accounts/signup/', params)

        self.assertIsInstance(User.objects.last().profile, Profile)
