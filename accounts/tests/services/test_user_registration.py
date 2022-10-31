from django.contrib.auth.models import User
from django.test import TestCase

from accounts.forms import SignUpForm
from accounts.models import Legal, Natural, Profile
from accounts.services.user_registration import UserRegistration

class UserRegistrationTestsWithValidParams(TestCase):
    def setUp(self):
        self.valid_params = {
            'username': 'fritazoid',
            'first_name': 'frite',
            'last_name': 'patatos',
            'profile_type': 'Natural',
            'password1': 'p@ssword1',
            'password2': 'p@ssword1',
        }

    def test_creates_a_user(self):
        UserRegistration.perform(SignUpForm(self.valid_params))

        self.assertEqual(User.objects.count(), 1)

    def test_creates_a_profile(self):
        UserRegistration.perform(SignUpForm(self.valid_params))

        self.assertEqual(Profile.objects.count(), 1)

    def test_associates_user_with_natural_profile(self):
        self.valid_params['profile_type'] = 'Natural'
        form = SignUpForm(self.valid_params)

        UserRegistration.perform(form)

        self.assertIsInstance(User.objects.last().profile, Natural)

    def test_associates_user_with_legal_profile(self):
        self.valid_params['profile_type'] = 'Legal'
        form = SignUpForm(self.valid_params)

        UserRegistration.perform(form)

        self.assertIsInstance(User.objects.last().profile, Legal)

    def test_with_invalid_params_does_not_create_a_user(self):
        self.valid_params['profile_type'] = ''

        UserRegistration.perform(SignUpForm(self.valid_params))

        self.assertEqual(User.objects.count(), 0)

    def test_with_invalid_params_does_not_create_a_profile(self):
        self.valid_params['profile_type'] = ''

        UserRegistration.perform(SignUpForm(self.valid_params))

        self.assertEqual(User.objects.count(), 0)
