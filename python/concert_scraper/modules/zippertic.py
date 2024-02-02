"""Fetch data from spelalive.nu"""

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time
from datetime import datetime
from concert_scraper.common import Concert
from concert_scraper.logger import get_logger

logger = get_logger(__name__)

BASE_URL = "https://spelalive.nu"


def parse_date(date_string):
    # Sat. Jan 20, 20:00
    date = datetime.strptime(date_string, '%a. %b %d, %H:%M')
    return date.strftime("%Y-%m-%d %H:%M")


def get_concerts(venue, browser):
    logger.info(f"Getting concerts for venue {venue.name} to {venue.url}")
    browser.get(venue.url)

    html = browser.page_source
    soup = BeautifulSoup(html)
    entries = soup.find_all("entry")
    breakpoint()
    concerts = []

    logger.info(len(entries))

    for concert in entries:
        concert_title = concert.find('div', attrs={'class': 'card-title'}).getText().strip()
        info = concert.find_all('div', attrs={'class': 'event-info-line'})
        concert_venue = info[0].getText().strip()
        concert_date = parse_date(info[1].getText().strip())
        logger.info(concert_venue)
        logger.info(concert_date)
        concert_url = concert.find('div', attrs={'class':'card-title'}).find('a').get('href')

        if concert_venue != venue.name:
            continue

        concerts.append(
            Concert(concert_title, concert_date, venue.name, concert_url)
        )
    logger.info(f"Found {len(concerts)} concerts for venue {venue.name}")
    return concerts
