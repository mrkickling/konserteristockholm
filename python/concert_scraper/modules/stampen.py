"""Fetch data from stampen.se"""

from datetime import datetime

from bs4 import BeautifulSoup

from ..common import Concert, get_future_date
from ..logger import get_logger

logger = get_logger(__name__)
BASE_URL = "https://www.stampen.se/program/"


def parse_date(date_string):
    # 31 Dec, 17:00 - 01:00
    date, month, *rest = date_string.split()

    try:
        date = datetime.strptime(f"{date} {month}", '%d %b,')
    except Exception:
        logger.info("No matching date string %s %s - trying without comma", date, month)
        date = datetime.strptime(f"{date} {month}", '%d %b')

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
        concert_title = card.find('h4', attrs={'class': 'mec-event-titlee'}).getText().strip()
        concert_date = parse_date(card.find('span', attrs={'class': 'mec-event-d'}).getText().strip())
        url_obj = card.find('a')
        concert_url = BASE_URL
        if url_obj:
            concert_url = card.find('a').get('href')
        concerts.append(
            Concert(concert_title, concert_date, venue.name, concert_url)
        )
    logger.info(f"Found {len(concerts)} concerts for venue {venue.name}")
    return concerts
