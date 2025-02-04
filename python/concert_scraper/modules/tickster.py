"""Fetch data from tickster.com"""

from datetime import datetime

from bs4 import BeautifulSoup

from ..common import Concert
from ..logger import get_logger
from .utils import short_months_se

logger = get_logger(__name__)
BASE_URL = "https://tickster.com"


def parse_date(date_string):
    # 29 mar 2024
    day, month, year = date_string.split()
    month_int = short_months_se.index(month) + 1
    day_int = int(day)
    year_int = int(year)

    return datetime(year_int, month_int, day_int).strftime("%Y-%m-%d")


def get_concerts(venue, browser):
    logger.info(f"Getting concerts for venue {venue.name}")
    browser.get(venue.url)
    html = browser.page_source

    def clean_date(date_str):
        dates = date_str.split(",")
        start_date = dates[0].strip()
        return start_date

    soup = BeautifulSoup(html, features="html.parser")
    cards = soup.find_all(name="div", attrs={'class': 'c-tile'})
    concerts = []
    for card in cards:
        concert_title = card.find('h2').getText().strip()
        date_attrs = {'class': 'c-tile__label'}
        concert_date = clean_date(
            card.find('span', attrs=date_attrs).getText())
        concert_url = BASE_URL + card.find('a').get('href')
        concerts.append(
            Concert(concert_title, parse_date(concert_date), venue.name, concert_url)
        )
    logger.info(f"Found {len(concerts)} concerts for venue {venue.name}")
    return concerts
