"""Fetch data from https://www.glennmillercafe.se"""

from datetime import datetime

from bs4 import BeautifulSoup

from ..common import Concert
from ..logger import get_logger

logger = get_logger(__name__)
BASE_URL = "https://www.glennmillercafe.se"

def parse_date(date_string):
    return datetime.strptime(date_string, '%Y-%m-%d').strftime("%Y-%m-%d")

def get_concerts(venue, browser):
    logger.info(f"Getting concerts for venue {venue.name}")
    browser.get(venue.url)
    html = browser.page_source

    soup = BeautifulSoup(html, features="html.parser")
    cards = soup.find_all(name="div", attrs={'class': 'konsert'})
    concerts = []
    for card in cards:
        concert_title = card.find('p', attrs={'class': 'artist'}).getText()
        concert_date = parse_date(card.find('p', attrs={'class': 'date'}).getText())
        concert_url = venue.url
        concerts.append(
            Concert(concert_title, concert_date, venue.name, concert_url)
        )

    logger.info(f"Found {len(concerts)} concerts for venue {venue.name}")
    return concerts
