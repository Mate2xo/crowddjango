from django.urls import reverse
import pytest

from accounts.tests.factories.users import UserFactory
from accounts.tests.factories.profiles import NaturalFactory


def test_required_login(client):
    response = client.get(reverse('accounts:profile_show'))
    assert '/accounts/login' in response.url


@pytest.mark.django_db
def test_http_ok_status(client):
    user = UserFactory()
    NaturalFactory(user=user)

    client.login(username=user.username, password='passpass')
    response = client.get(reverse('accounts:profile_show'))

    assert response.status_code == 200
