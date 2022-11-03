import pytest

from investments.models import Fund
from investments.tests.factories.funds import FundFactory


@pytest.fixture
def _fund():
    return FundFactory.build()


def test_string_representation(_fund):
    assert str(_fund) == _fund.name


def test_default_status(_fund):
    assert _fund.status == Fund.Status.BEING_CREATED
