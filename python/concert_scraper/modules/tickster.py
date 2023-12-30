"""Fetch data from tickster.com"""

from bs4 import BeautifulSoup
from datetime import datetime
from concert_scraper.common import Concert
from concert_scraper.logger import get_logger

logger = get_logger(__name__)

BASE_URL = "https://tickster.com"


def parse_date(date_string):
    # 29 mar 2024
    return datetime.strptime(date_string, '%d %b %Y')


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
    concerts = set()
    for card in cards:
        concert_title = card.find('h2').getText().strip()
        date_attrs = {'class': 'c-tile__label'}
        concert_date = clean_date(
            card.find('span', attrs=date_attrs).getText())
        concert_url = BASE_URL + card.find('a').get('href')
        concerts.add(
            Concert(concert_title, concert_date, venue.name, concert_url)
        )
    logger.info(f"Found {len(concerts)} concerts for venue {venue.name}")
    return concerts
