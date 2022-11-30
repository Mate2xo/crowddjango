from django.contrib.auth.models import User
from django.core import mail
from django.utils.text import gettext_lazy as _
import pytest

from accounts.forms import LegalProfileForm, NaturalProfileForm, SignUpForm
from accounts.models import Legal, Natural, Profile
from accounts.services.user_registration import UserRegistration


@pytest.fixture
def user_params():
    return {'username': 'fritazoid',
            'first_name': 'frite',
            'last_name': 'patatos',
            'password1': 'p@ssword1',
            'password2': 'p@ssword1'}


@pytest.fixture
def profile_params():
    return {'email': 'oh@my.god',
            'profile_type': 'Natural'}


@pytest.mark.django_db
def test_creates_a_user(user_params, profile_params):
    UserRegistration.perform(SignUpForm(user_params), NaturalProfileForm(profile_params))

    assert User.objects.count() == 1


@pytest.mark.django_db
def test_creates_a_profile(user_params, profile_params):
    UserRegistration.perform(SignUpForm(user_params), NaturalProfileForm(profile_params))

    assert Profile.objects.count() == 1


@pytest.mark.django_db
def test_sends_a_welcome_email(user_params, profile_params):
    UserRegistration.perform(SignUpForm(user_params), NaturalProfileForm(profile_params))

    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == _('Welcome to VoyagesPasCher')


class TestWithANaturalProfile:
    @pytest.mark.django_db
    def test_associates_user_with_natural_profile(self, user_params, profile_params):
        profile_params['profile_type'] = 'Natural'

        UserRegistration.perform(SignUpForm(user_params), NaturalProfileForm(profile_params))

        assert type(User.objects.last().profile) == Natural


class TestWithALegalProfile:
    @pytest.mark.django_db
    def test_associates_user_with_legal_profile(self, user_params, profile_params):
        profile_params['profile_type'] = 'Legal'

        UserRegistration.perform(SignUpForm(user_params), LegalProfileForm(profile_params))

        assert type(User.objects.last().profile) == Legal


class TestWithInvalidParams:
    @pytest.fixture
    def invalid_params(self, profile_params):
        invalid_params = profile_params | {'profile_type': ''}
        return invalid_params

    @pytest.mark.django_db
    def test_with_does_not_create_a_user(self, invalid_params, profile_params):
        UserRegistration.perform(SignUpForm(invalid_params), NaturalProfileForm(profile_params))

        assert User.objects.count() == 0

    @pytest.mark.django_db
    def test_with_does_not_create_a_profile(self, invalid_params, profile_params):
        UserRegistration.perform(SignUpForm(invalid_params), NaturalProfileForm(profile_params))

        assert Profile.objects.count() == 0

    @pytest.mark.django_db
    def test_does_not_send_welcome_email(self, invalid_params, profile_params):
        UserRegistration.perform(SignUpForm(invalid_params), NaturalProfileForm(profile_params))

        assert len(mail.outbox) == 0


class TestWhenProfileCreationFails:
    @pytest.mark.django_db
    def test_user_creation_is_rollbacked(self, mocker, user_params, profile_params):
        def create_user_profile_mock(input):
            raise RuntimeError('BOOM')

        mocker.patch('accounts.services.UserRegistration.create_user_profile',
                     create_user_profile_mock)

        with pytest.raises(RuntimeError):
            UserRegistration.perform(SignUpForm(user_params), NaturalProfileForm(profile_params))

        assert User.objects.count() == 0
