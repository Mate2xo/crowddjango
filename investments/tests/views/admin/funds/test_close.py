from django.contrib.admin.options import messages
from django.urls import reverse
import pytest

from investments.models.fund import Fund
from investments.tests.factories.funds import FundFactory


@pytest.fixture
def closable_fund():
    return FundFactory(closable=True)


@pytest.mark.django_db
def test_get_is_404_http_status(closable_fund, admin_client):
    response = admin_client.get(reverse('admin:investments_fund_close', args=[closable_fund.id]))

    assert response.status_code == 404


@pytest.mark.django_db
def test_post_redirects_to_funds_list(closable_fund, admin_client):
    response = admin_client.post(reverse('admin:investments_fund_close', args=[closable_fund.id]))

    assert response.url == reverse('admin:investments_fund_changelist')


class TestWithAnUnclosableFund:
    @pytest.fixture
    def unclosable_fund(self):
        return FundFactory(published=True)

    @pytest.mark.django_db
    def test_does_not_update_status(self, unclosable_fund, admin_client):
        original_status = unclosable_fund.status

        admin_client.post(reverse('admin:investments_fund_close', args=[unclosable_fund.id]))

        unclosable_fund.refresh_from_db()
        assert unclosable_fund.status == original_status

    @pytest.mark.django_db
    def test_validation_feedback(self, unclosable_fund, admin_client):
        response = admin_client.post(reverse('admin:investments_fund_close', args=[unclosable_fund.id]))

        error_msgs = list(map(lambda obj: obj.message, messages.get_messages(response.wsgi_request)))
        assert 'closing_date' in error_msgs[0]

    @pytest.mark.django_db
    def test_redirects_to_fund_change(self, unclosable_fund, admin_client):
        response = admin_client.post(reverse('admin:investments_fund_close', args=[unclosable_fund.id]))
        assert response.url == reverse('admin:investments_fund_change', args=[unclosable_fund.id])


class TestWithAClosableFund:
    @pytest.mark.django_db
    def test_updates_status_to_close(self, closable_fund, admin_client):
        admin_client.post(reverse('admin:investments_fund_close', args=[closable_fund.id]))

        closable_fund.refresh_from_db()
        assert closable_fund.status == Fund.Status.CLOSED
