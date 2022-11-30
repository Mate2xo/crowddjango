from django.test import TestCase
import pytest

from accounts.forms import SignUpForm


@pytest.mark.django_db
def test_with_invalid_params():
    data = {'username': ''}
    form = SignUpForm(data)
    assert form.is_valid() is False


@pytest.mark.django_db
def test_with_valid_params():
    data = {
        'username': 'polo_et_pan',
        'first_name': 'polo',
        'last_name': 'pan',
        'password1': 'P@assword1',
        'password2': 'P@assword1',
        'profile_type': 'Natural'
    }
    form = SignUpForm(data)
    assert form.is_valid() is True
