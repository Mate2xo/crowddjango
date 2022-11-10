from datetime import date, timedelta
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django_fsm import TransitionNotAllowed
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

    def test_transition_to_closed(self, _closable_fund):
        _closable_fund.close()
        assert _closable_fund.status == Fund.Status.CLOSED

    @pytest.mark.django_db
    def test_no_transition_without_closing_date_expiration(self, _closable_fund):
        _closable_fund.closing_date = date.today() + timedelta(days=1)
        with pytest.raises(TransitionNotAllowed):
            _closable_fund.close()

    @pytest.mark.django_db
    def test_closing_date_validation(self, _closable_fund):
        _closable_fund.status = Fund.Status.CLOSED
        _closable_fund.closing_date = date.today() + timedelta(days=1)
        with pytest.raises(ValidationError) as exception_info:
            _closable_fund.full_clean()

        assert _('Closing date has not expired yet') in exception_info.value.messages

    def test_fund_must_be_published(self, _closable_fund):
        _closable_fund.status = Fund.Status.BEING_CREATED
        with pytest.raises(TransitionNotAllowed):
            _closable_fund.close()


class TestWhenTransitionningToPublished:
    @pytest.fixture
    def _publishable_fund(self):
        return FundFactory.build(publishable=True)

    def test_transition_to_published(self, _publishable_fund):
        _publishable_fund.publish()
        assert _publishable_fund.status == Fund.Status.PUBLISHED

    @pytest.mark.django_db
    def test_no_transition_without_closing_date_presence(self, _publishable_fund):
        _publishable_fund.closing_date = None
        with pytest.raises(TransitionNotAllowed):
            _publishable_fund.publish()

    @pytest.mark.django_db
    def test_no_transition_without_goal_presence(self, _publishable_fund):
        _publishable_fund.goal = None
        with pytest.raises(TransitionNotAllowed):
            _publishable_fund.publish()

    @pytest.mark.django_db
    def test_closing_date_presence(self, _publishable_fund):
        _publishable_fund.status = Fund.Status.PUBLISHED
        _publishable_fund.closing_date = None

        with pytest.raises(ValidationError) as exception_info:
            _publishable_fund.full_clean()

        assert _('Closing date field is required') in exception_info.value.messages

    @pytest.mark.django_db
    def test_goal_presence(self, _publishable_fund):
        _publishable_fund.status = Fund.Status.PUBLISHED
        _publishable_fund.goal = None

        with pytest.raises(ValidationError) as exception_info:
            _publishable_fund.full_clean()

        assert _('Goal field is required') in exception_info.value.messages

    @pytest.mark.django_db
    def test_closing_date_and_goal_presence_feedback(self, _publishable_fund):
        _publishable_fund.status = Fund.Status.PUBLISHED
        _publishable_fund.closing_date = None
        _publishable_fund.goal = None

        with pytest.raises(ValidationError) as exception_info:
            _publishable_fund.full_clean()

        assert _('Closing date field is required') in exception_info.value.messages
        assert _('Goal field is required') in exception_info.value.messages
