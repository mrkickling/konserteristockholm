from datetime import datetime
from concert_scraper.modules import billetto, glenmiller, konserthuset, nortic, scala, stampen, tickster

def test_billetto_date():
    current_year = datetime.now().year
    date_string = "10 May . 10:23"
    result = billetto.parse_date(date_string)
    assert result == datetime(current_year + 1, 5, 10)

def test_glenmiller_date():
    date_string = "2023-12-01"
    result = glenmiller.parse_date(date_string)
    assert result == datetime(2023, 12, 1)

def test_konserthuset_date():
    date_string = 'Fredag 5 januari 2024 kl 17.00'
    result = konserthuset.parse_date(date_string)
    assert result == datetime(2024, 1, 5)

def test_nortic_date():
    date_string = '5 January'
    result = nortic.parse_date(date_string)
    assert result == datetime(2024, 1, 5)

def test_scala_date():
    date_string = '5 jan'
    result = scala.parse_date(date_string)
    assert result == datetime(2024, 1, 5)

def test_stampen_date():
    date_string = '31 Dec, 17:00 - 01:00'
    result = stampen.parse_date(date_string)
    assert result == datetime(2023, 12, 31)

def test_tickster_date():
    date_string = '29 mar 2024'
    result = tickster.parse_date(date_string)
    assert result == datetime(2024, 3, 29)