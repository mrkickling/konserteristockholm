from datetime import datetime
from concert_scraper.modules import billetto, glenmiller, konserthuset, nortic, scala, stampen, tickster
from concert_scraper.common import get_future_date
from unittest import mock

@mock.patch("concert_scraper.common.get_current_date")
def test_billetto_date(mocked_date):
    mocked_date.return_value = datetime(2024, 1, 1)
    date_string = "10 maj. 10:23"
    result = billetto.parse_date(date_string)
    assert result == "2024-05-10"

def test_glenmiller_date():
    date_string = "2023-12-01"
    result = glenmiller.parse_date(date_string)
    assert result == "2023-12-01"

@mock.patch("concert_scraper.common.get_current_date")
def test_konserthuset_date(mocked_date):
    mocked_date.return_value = datetime(2024, 1, 1)
    date_string = 'Fredag 5 januari 2024 kl 17.00'
    result = konserthuset.parse_date(date_string)
    assert result == "2024-01-05"

@mock.patch("concert_scraper.common.get_current_date")
def test_nortic_date(mocked_date):
    mocked_date.return_value = datetime(2024, 1, 1)
    date_string = '5 January'
    result = nortic.parse_date(date_string)
    assert result == "2024-01-05"

@mock.patch("concert_scraper.common.get_current_date")
def test_scala_date(mocked_date):
    mocked_date.return_value = datetime(2024, 1, 1)
    date_string = '5 jan'
    result = scala.parse_date(date_string)
    assert result == "2024-01-05"

@mock.patch("concert_scraper.common.get_current_date")
def test_stampen_date(mocked_date):
    mocked_date.return_value = datetime(2024, 12, 1)
    date_string = '31 Dec, 17:00 - 01:00'
    result = stampen.parse_date(date_string)
    assert result == "2024-12-31"

def test_tickster_date():
    date_string = '29 mar 2024'
    result = tickster.parse_date(date_string)
    assert result == "2024-03-29"

@mock.patch("concert_scraper.common.get_current_date")
def test_get_future_date(mocked_date):
    mocked_date.return_value = datetime(2024, 1, 1)
    assert get_future_date(1, 1) == datetime(2024, 1, 1)
    assert get_future_date(5, 5) == datetime(2024, 5, 5)
    assert get_future_date(10, 10) == datetime(2024, 10, 10)

    mocked_date.return_value = datetime(2024, 6, 6)
    assert get_future_date(6, 6) == datetime(2024, 6, 6)
    assert get_future_date(1, 1) == datetime(2025, 1, 1)
    assert get_future_date(5, 5) == datetime(2025, 5, 5)
    assert get_future_date(2, 29) == datetime(2024, 2, 29)