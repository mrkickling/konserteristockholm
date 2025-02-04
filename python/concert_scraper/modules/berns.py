"""Module for venue Berns"""

from datetime import datetime

from bs4 import BeautifulSoup

from ..common import Concert
from ..logger import get_logger
from .utils import months_se

logger = get_logger(__name__)
BASE_URL = "https://berns.se/sv/kalender"


def parse_date(date_string):
    """Convert from Berns format"""
    date, month, year = date_string.split()
    date_int = int(date)
    month_int = months_se.index(month.lower()) + 1
    year_int = int(year)
    return datetime(year_int, month_int, date_int).strftime("%Y-%m-%d")


def get_concerts(venue, browser):
    logger.info(f"Getting concerts for venue {venue.name}")
    browser.get(venue.url)

    concerts = []

    # Scroll to bottom
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    html = browser.page_source
    soup = BeautifulSoup(html, features="html.parser")

    # All concert sections have the class event-card-2
    concert_elements = soup.find_all("div", attrs={'class': 'calender-item'})
    for concert in concert_elements:
        try:
            concert_title = concert.find('div', attrs={'class': 'citem-title'}).getText().strip()
            concert_date = parse_date(concert.find('div', attrs={'class': 'citem-date'}).getText().strip())
            concert_url = concert.parent.parent.find('a').get('href')

            concerts.append(
                Concert(concert_title, concert_date, venue.name, concert_url)
            )
        except ValueError as e:
            logger.error("Failed to add concert")

    logger.info(f"Found {len(concerts)} concerts for venue {venue.name}")
    return concerts
