"""Fetch data from https://www.lykkenytorget.se/lykke-live"""

from bs4 import BeautifulSoup

from ..common import Concert
from ..logger import get_logger

logger = get_logger(__name__)
BASE_URL = "https://www.lykkenytorget.se/lykke-live/"


def get_concerts(venue, browser):
    logger.info(f"Getting concerts for venue {venue.name}")
    browser.get(venue.url)
    html = browser.page_source

    soup = BeautifulSoup(html, features="html.parser")

    cards = soup.find_all("article", attrs={'class': 'eventlist-event'})
    concerts = []

    for card in cards:
        concert_title = card.find('h1').getText()
        concert_date = card.find(
                'time',
                attrs={'class': 'event-time-localized-start'}
            ).get('datetime')

        concert_url = card.find('a').get('href')
        concerts.append(
            Concert(concert_title, concert_date, venue.name, concert_url)
        )

    logger.info(f"Found {len(concerts)} concerts for venue {venue.name}")
    return concerts
