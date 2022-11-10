from django.contrib.admin.options import messages
from django.urls import reverse
import pytest

from investments.models.fund import Fund
from investments.tests.factories.funds import FundFactory


@pytest.fixture
def publishable_fund():
    return FundFactory(publishable=True)


@pytest.mark.django_db
def test_get_is_404_http_status(publishable_fund, admin_client):
    response = admin_client.get(reverse('admin:investments_fund_publish', args=[publishable_fund.id]))

    assert response.status_code == 404


@pytest.mark.django_db
def test_post_redirects_to_funds_list(publishable_fund, admin_client):
    response = admin_client.post(reverse('admin:investments_fund_publish', args=[publishable_fund.id]))

    assert response.url == reverse('admin:investments_fund_changelist')


class TestWithAnUnpublishableFund:
    @pytest.fixture
    def unpublishable_fund(self):
        return FundFactory()

    @pytest.mark.django_db
    def test_does_not_update_status(self, unpublishable_fund, admin_client):
        original_status = unpublishable_fund.status

        admin_client.post(reverse('admin:investments_fund_publish', args=[unpublishable_fund.id]))

        unpublishable_fund.refresh_from_db()
        assert unpublishable_fund.status == original_status

    @pytest.mark.django_db
    def test_validation_feedback(self, unpublishable_fund, admin_client):
        response = admin_client.post(reverse('admin:investments_fund_publish', args=[unpublishable_fund.id]))

        error_msgs = list(map(lambda obj: obj.message, messages.get_messages(response.wsgi_request)))
        assert 'closing_date' in error_msgs[0]
        assert 'goal' in error_msgs[1]


class TestWithAPublishableFund:
    @pytest.mark.django_db
    def test_updates_status_to_published(self, publishable_fund, admin_client):
        admin_client.post(reverse('admin:investments_fund_publish', args=[publishable_fund.id]))

        publishable_fund.refresh_from_db()
        assert publishable_fund.status == Fund.Status.PUBLISHED
