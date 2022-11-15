from django.test import TestCase

from accounts.forms import SignUpForm


class SignUpFormTest(TestCase):
    def test_with_invalid_params(self):
        data = {'username': ''}
        form = SignUpForm(data)
        self.assertFalse(form.is_valid())

    def test_with_valid_params(self):
        data = {
            'username': 'polo_et_pan',
            'first_name': 'polo',
            'last_name': 'pan',
            'password1': 'P@assword1',
            'password2': 'P@assword1',
            'profile_type': 'Natural'
        }
        form = SignUpForm(data)
        self.assertTrue(form.is_valid())
