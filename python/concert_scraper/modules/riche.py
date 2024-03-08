"""Fetch data from riche.se"""

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
from bs4 import BeautifulSoup
import time

from concert_scraper.common import Concert, get_future_date
from concert_scraper.logger import get_logger

logger = get_logger(__name__)

BASE_URL = "https://riche.se/kalendarium"

def parse_date(date_string):
    # Torsdag 8/02
    date_string = date_string.split()[1]
    day, month = date_string.split('/')
    month_int = int(month)
    day_int = int(day)
    date = get_future_date(month_int, day_int)
    return date.strftime("%Y-%m-%d")

def get_concerts(venue, browser):
    logger.info(f"Getting concerts for venue {venue.name}")
    browser.get(venue.url)

    # cookie_action_close_header
    time.sleep(4)
    button = browser.find_element(By.CLASS_NAME, "cky-btn-accept")
    button.click()

    # 'Load more' as many times as possible
    try:
        time.sleep(1)
        button = browser.find_element(By.CLASS_NAME, "load-more-events")
        while button.is_displayed():
            logger.info("Loading more...")
            button.click()
            time.sleep(1)
    except NoSuchElementException:
        logger.info("No more events to load")

    html = browser.page_source
    soup = BeautifulSoup(html, features="html.parser")
    cards = soup.find_all("article", attrs={'class': 'event'})

    concerts = []
    for card in cards:
        concert_title = card.find('h6', attrs={'class': 'event-title'}).getText().strip()
        concert_date = card.find(attrs={'class': 'event-date'}).getText().strip()
        concert_url = card.find('a').get('href')
        event_type = card.find('span', {'class': 'event-type'}).getText()[3:]
        if event_type in ('DJ', 'Live'):
            concerts.append(
                Concert(concert_title, parse_date(concert_date), venue.name, concert_url)
            )
    logger.info(f"Found {len(concerts)} concerts for venue {venue.name}")
    return concerts
