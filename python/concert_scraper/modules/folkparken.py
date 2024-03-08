"""Fetch data from https://www.restaurangfolkparken.se"""

from bs4 import BeautifulSoup
from datetime import datetime
import re

from concert_scraper.common import Concert, get_future_date
from concert_scraper.logger import get_logger

logger = get_logger(__name__)

BASE_URL = "https://www.restaurangfolkparken.se"

def parse_date(date_string):
    # 03/01
    day, month = date_string.split('/')
    month_int = int(month)
    day_int = int(day)
    date = get_future_date(month_int, day_int)

    return date.strftime("%Y-%m-%d")

def get_concerts(venue, browser):
    logger.info(f"Getting concerts for venue {venue.name}")
    browser.get(venue.url)
    html = browser.page_source

    concerts = []
    soup = BeautifulSoup(html, features='html.parser')
    potential_concerts = soup.find_all('p')
    for potential in potential_concerts:
        text = potential.getText()
        pattern = re.compile('.* \d+\/\d+ .*')
        hit = pattern.match(text)
        if hit:
            concert = hit.group()
            day, date, *concert_title_parts = concert.split()
            concert_title = " ".join(concert_title_parts)
            concert_date = parse_date(date)
            concert_url = venue.url
            concerts.append(
                Concert(concert_title, concert_date, venue.name, concert_url)
            )

    logger.info(f"Found {len(concerts)} concerts for venue {venue.name}")
    return concerts
