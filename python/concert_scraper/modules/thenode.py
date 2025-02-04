"""Module for venue The Node"""
import time

from bs4 import BeautifulSoup

from ..common import Concert, get_future_date
from ..logger import get_logger
from .utils import short_months_en

logger = get_logger(__name__)
BASE_URL = "https://thenode.se"


def parse_date(date_string):
    """Convert from Berns format"""
    date, month, *_ = date_string.split()
    date_int = int(date)
    month_int = short_months_en.index(month.lower()) + 1
    date = get_future_date(month_int, date_int)
    return date.strftime("%Y-%m-%d")


def get_concerts(venue, browser):
    logger.info(f"Getting concerts for venue {venue.name}")
    browser.get(venue.url)

    concerts = []

    # Scroll to bottom
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(2)
    html = browser.page_source
    soup = BeautifulSoup(html, features="html.parser")
    concert_elements = soup.find_all("a", attrs={'class': 'summary-link'})
    for concert in concert_elements:
        try:
            concert_title_obj = concert.find_next_sibling('p', attrs={'class': 'h3'})
            concert_title = concert_title_obj.getText().strip()
            concert_date = parse_date(concert_title_obj.find_next_sibling('p').getText().strip())
            concert_url = BASE_URL + concert.parent.parent.find('a').get('href')

            concerts.append(
                Concert(concert_title, concert_date, venue.name, concert_url)
            )
        except ValueError as e:
            logger.error("Failed to add concert")

    logger.info(f"Found {len(concerts)} concerts for venue {venue.name}")
    return concerts
