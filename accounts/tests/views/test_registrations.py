from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
import pytest

from pytest_django.asserts import assertRedirects, assertTemplateUsed
from returns.result import Failure, Success


class SignUpGet(TestCase):
    def test_http_ok_status(self):
        response = self.client.get(reverse('accounts:signup'))

        self.assertEqual(response.status_code, 200)


class TestSignUpPost():
    @pytest.fixture
    def valid_params(self):
        return {
            'username': 'polo_et_pan',
            'first_name': 'polo',
            'last_name': 'pan',
            'password1': 'P@assword1',
            'password2': 'P@assword1',
            'profile_type': 'Legal',
            'email': 'dans@la.canopée'
        }

    @pytest.mark.django_db
    def test_with_successful_user_registration_redirects_to_login(self, valid_params, client):
        response = client.post('/accounts/signup/', valid_params)

        assertRedirects(response, reverse('login'))

    @pytest.mark.django_db
    def test_with_failed_user_registration_redirects_to_signup(self, valid_params, client):
        invalid_params = valid_params | {'profile_type': ''}

        response = client.post('/accounts/signup/', invalid_params)

        assertTemplateUsed(response, 'registration/signup.html')
