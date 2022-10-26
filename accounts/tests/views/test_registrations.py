from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch

class SignUpGet(TestCase):
    def test_http_ok_status(self):
        response = self.client.get(reverse('accounts:signup'))

        self.assertEqual(response.status_code, 200)

class SignUpPost(TestCase):
    def setUp(self):
        self.valid_params = {
            'username': 'polo_et_pan',
            'first_name': 'polo',
            'last_name': 'pan',
            'password1': 'P@assword1',
            'password2': 'P@assword1',
            'profile_type': 'Legal'
        }

    @patch('accounts.services.UserRegistration.perform', autospec=True)
    def test_with_successful_user_registration_redirects_to_login(self, mocked_method):
        mocked_method.return_value = True

        response = self.client.post('/accounts/signup/', self.valid_params)

        assert mocked_method.called
        self.assertRedirects(response, reverse('login'))

    @patch('accounts.services.UserRegistration.perform', autospec=True)
    def test_with_failed_user_registration_redirects_to_signup(self, mocked_method):
        mocked_method.return_value = False
        invalid_params = self.valid_params
        invalid_params['profile_type'] = ''

        response = self.client.post('/accounts/signup/', invalid_params)

        assert mocked_method.called
        self.assertTemplateUsed(response, 'registration/signup.html')
