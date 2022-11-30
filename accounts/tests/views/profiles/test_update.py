from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.handlers.asgi import tempfile
from django.urls import reverse
import pytest

from accounts.tests.factories.profiles import NaturalFactory
from accounts.tests.factories.users import UserFactory


@pytest.fixture
def non_file_params():
    return {'csrfmiddlewaretoken': ['x0g7T80E4v243SEpL3b7PpwOKzrdA0YUgsTPDsInXWIGNSqbtSJR3lBmHh448jRu'],
            'email': ['test@test.test'],
            'phone_number': ['21434123'],
            'place_of_birth': 'over the rainbow'}


def test_required_login(client):
    response = client.get(reverse('accounts:profile_edit'))
    assert '/accounts/login' in response.url


@pytest.mark.django_db
def test_edit_has_ok_http_status(client):
    user = UserFactory(with_any_profile=True)
    client.login(username=user.username, password='passpass')

    response = client.get(reverse('accounts:profile_edit'))

    assert response.status_code == 200


@pytest.mark.django_db
def test_update_has_ok_http_status(client):
    user = UserFactory(with_any_profile=True)
    client.login(username=user.username, password='passpass')

    response = client.post(reverse('accounts:profile_edit'))

    assert response.status_code == 200


class TestWithAvatarParams():
    @pytest.fixture(autouse=True)
    def before(self, settings, tmp_path):
        settings.MEDIA_ROOT = tmp_path  # Model upload actually writes the new file to storage

    @pytest.mark.django_db(transaction=True)
    def test_creates_a_new_file_for_user_without_avatar(self, client, non_file_params):
        user_without_avatar = UserFactory(with_natural_profile=True)
        client.login(username=user_without_avatar.username, password='passpass')

        with open('accounts/tests/fixtures/files/logo.png', 'rb') as f:
            client.post(reverse('accounts:profile_edit'), non_file_params | {'avatar': f})
        user_without_avatar.refresh_from_db()

        avatar = user_without_avatar.profile.avatar
        assert bool(avatar) is True
        assert avatar.storage.exists(avatar.name)


class TestWithExistingAvatar():
    @pytest.fixture
    def tmp_img(self):
        with tempfile.NamedTemporaryFile(suffix='.png') as img:
            yield img

    @pytest.fixture
    def user_with_avatar(self, tmp_img, settings, tmp_path):
        settings.MEDIA_ROOT = tmp_path  # Model upload actually writes the new file to storage
        user_with_avatar = UserFactory()
        NaturalFactory(user=user_with_avatar, avatar=SimpleUploadedFile(tmp_img.name, tmp_img.read(), 'image/png'))
        return user_with_avatar

    @pytest.fixture(autouse=True)
    def before(self, settings, tmp_path, user_with_avatar, client):
        settings.MEDIA_ROOT = tmp_path  # Model upload actually writes the new file to storage
        client.login(username=user_with_avatar.username, password='passpass')

    @pytest.mark.django_db(transaction=True)  # @see https://github.com/un1t/django-cleanup#how-to-write-tests
    def test_removing_avatar_deletes_its_file(self, client, non_file_params, user_with_avatar):
        filename = user_with_avatar.profile.avatar.name

        client.post(reverse('accounts:profile_edit'), non_file_params | {'avatar-clear': 'on'})

        user_with_avatar.refresh_from_db()
        avatar = user_with_avatar.profile.avatar
        assert bool(avatar) is False
        assert not avatar.storage.exists(filename)

    @pytest.mark.django_db(transaction=True)
    def test_replacing_avatar_creates_a_new_file_and_deletes_the_old_one(self,
                                                                         client,
                                                                         non_file_params,
                                                                         user_with_avatar):
        old_avatar_name = user_with_avatar.profile.avatar.name

        with open('accounts/tests/fixtures/files/logo.png', 'rb') as f:
            client.post(reverse('accounts:profile_edit'), non_file_params | {'avatar': f})
        user_with_avatar.refresh_from_db()

        avatar = user_with_avatar.profile.avatar
        assert bool(avatar)
        assert not avatar.storage.exists(old_avatar_name)
        assert avatar.storage.exists(avatar.name)
