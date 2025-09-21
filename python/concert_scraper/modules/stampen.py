"""Fetch data from stampen.se"""

from datetime import datetime

from bs4 import BeautifulSoup

from ..common import Concert, get_future_date
from ..logger import get_logger

logger = get_logger(__name__)
BASE_URL = "https://www.stampen.se/program/"


def parse_date(date_string: str):
    # 07 - 20 SEP
    # or 25 SEP
    if '-' in date_string:
        return None

    day, month, *rest = date_string.split()
    date = datetime.strptime(f"{day} {month}", '%d %b')

    date = get_future_date(date.month, date.day)
    return date.strftime("%Y-%m-%d")


def get_concerts(venue, browser):
    logger.info(f"Getting concerts for venue {venue.name}")
    browser.get(venue.url)
    html = browser.page_source

    soup = BeautifulSoup(html, features="html.parser")
    cards = soup.find_all(name="article", attrs={'class': 'mec-event-article'})
    concerts = []
    for card in cards:
        concert_title = card.find('h3', attrs={'class': 'mec-event-title'}).getText().strip()
        concert_date = parse_date(card.find('span', attrs={'class': 'mec-event-d'}).getText().strip())

        if not concert_date:
            continue

        url_obj = card.find('a')
        concert_url = BASE_URL
        if url_obj:
            concert_url = card.find('a').get('href')
        concerts.append(
            Concert(concert_title, concert_date, venue.name, concert_url)
        )
    logger.info(f"Found {len(concerts)} concerts for venue {venue.name}")
    return concerts
