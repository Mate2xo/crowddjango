from django.contrib.auth.models import User
from django.test import TestCase
import pytest

from accounts.forms import SignUpForm
from accounts.models import Legal, Natural, Profile
from accounts.services.user_registration import UserRegistration


@pytest.fixture
def valid_params():
    return {'username': 'fritazoid',
            'first_name': 'frite',
            'last_name': 'patatos',
            'profile_type': 'Natural',
            'password1': 'p@ssword1',
            'password2': 'p@ssword1'}


@pytest.mark.django_db
def test_creates_a_user(valid_params):
    UserRegistration.perform(SignUpForm(valid_params))

    assert User.objects.count() == 1


@pytest.mark.django_db
def test_creates_a_profile(valid_params):
    UserRegistration.perform(SignUpForm(valid_params))

    assert Profile.objects.count() == 1


class TestWithANaturalProfile:
    @pytest.mark.django_db
    def test_associates_user_with_natural_profile(self, valid_params):
        valid_params['profile_type'] = 'Natural'
        form = SignUpForm(valid_params)

        UserRegistration.perform(form)

        assert type(User.objects.last().profile) == Natural


class TestWithALegalProfile:
    @pytest.mark.django_db
    def test_associates_user_with_legal_profile(self, valid_params):
        valid_params['profile_type'] = 'Legal'
        form = SignUpForm(valid_params)

        UserRegistration.perform(form)

        assert type(User.objects.last().profile) == Legal


class TestWithInvalidParams:
    @pytest.fixture
    def invalid_params(self, valid_params):
        invalid_params = valid_params | {'profile_type': ''}
        return invalid_params

    @pytest.mark.django_db
    def test_with_invalid_params_does_not_create_a_user(self, invalid_params):
        UserRegistration.perform(SignUpForm(invalid_params))

        assert User.objects.count() == 0

    @pytest.mark.django_db
    def test_with_invalid_params_does_not_create_a_profile(self, invalid_params):
        UserRegistration.perform(SignUpForm(invalid_params))

        assert Profile.objects.count() == 0


class TestWhenProfileCreationFails:
    @pytest.mark.django_db
    def test_user_creation_is_rollbacked(self, mocker, valid_params):
        def associate_user_and_profile_mock(user, form):
            raise RuntimeError('BOOM')

        mocker.patch('accounts.views.UserRegistration.associate_user_and_profile',
                     associate_user_and_profile_mock)

        with pytest.raises(RuntimeError):
            UserRegistration.perform(SignUpForm(valid_params))

        assert User.objects.count() == 0
