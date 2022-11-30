from django.urls import reverse
import pytest

from investments.tests.factories.funds import FundFactory


@pytest.fixture
def _fund():
    return FundFactory()


@pytest.mark.django_db
def test_get_is_200_http_status(_fund, admin_client):
    response = admin_client.get(reverse('admin:investments_fund_change', args=[_fund.id]))

    assert response.status_code == 200
