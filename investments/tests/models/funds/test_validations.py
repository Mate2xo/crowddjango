from datetime import date
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import pytest

from investments.models import Fund
from investments.tests.factories.funds import FundFactory


@pytest.fixture
def _fund():
    return FundFactory.build()


def test_name_presence():
    fund = FundFactory.build(name='')
    with pytest.raises(ValidationError):
        fund.clean_fields()


def test_default_status(_fund):
    assert _fund.status == Fund.Status.BEING_CREATED


class TestWhenTransitionningToClosed:
    @pytest.fixture
    def _closable_fund(self):
        return FundFactory.build(closable=True)

    @pytest.mark.django_db
    def test_closing_date_expiration(self, _closable_fund):
        _closable_fund.status = Fund.Status.CLOSED
        _closable_fund.closing_date = date.today()
        with pytest.raises(ValidationError) as exception_info:
            _closable_fund.full_clean()

        assert _('Closing date has not expired yet') in exception_info.value.messages


class TestWhenTransitionningToPublished:
    @pytest.fixture
    def _publishable_fund(self):
        return FundFactory.build(publishable=True)

    @pytest.mark.django_db
    def test_closing_date_presence(self, _publishable_fund):
        _publishable_fund.status = Fund.Status.PUBLISHED
        _publishable_fund.closing_date = None
        with pytest.raises(ValidationError):
            _publishable_fund.full_clean()

    @pytest.mark.django_db
    def test_closing_date_presence_feedback(self, _publishable_fund):
        _publishable_fund.status = Fund.Status.PUBLISHED
        _publishable_fund.closing_date = None
        with pytest.raises(ValidationError) as exception_info:
            _publishable_fund.full_clean()

        assert _('Closing date field is missing') in exception_info.value.messages

    @pytest.mark.django_db
    def test_goal_presence(self, _publishable_fund):
        _publishable_fund.status = Fund.Status.PUBLISHED
        _publishable_fund.goal = None
        with pytest.raises(ValidationError) as exception_info:
            _publishable_fund.full_clean()

        assert _('Goal field is missing') in exception_info.value.messages
