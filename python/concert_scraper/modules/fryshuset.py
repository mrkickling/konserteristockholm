# For https://fryshuset.se/konserter
import time
from datetime import datetime

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from ..common import Concert
from ..logger import get_logger
from .utils import short_months_se

logger = get_logger(__name__)
BASE_URL = "https://fryshuset.se"

def parse_date(date_string):
    # '28 feb 2024'
    date, month, year = date_string.split()
    date_int = int(date)
    month_int = short_months_se.index(month.lower()) + 1
    year_int = int(year)
    return datetime(year_int, month_int, date_int).strftime("%Y-%m-%d")

def get_concerts(venue, browser):
    logger.info(f"Getting concerts for venue {venue.name}")

    browser.get(venue.url)
    time.sleep(1) # Wait for cookie dialog

    try:
        browser.find_element(By.ID, 'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll').click()
    except Exception:
        logger.info("Could not find cookie window - might be fine")

    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1) # Wait for more to load
    html = browser.page_source

    soup = BeautifulSoup(html, features="html.parser")
    events = soup.find_all("div", attrs={'class': 'concert'})

    concerts = []
    for concert in events:
        concert = concert.parent # To get the anchor tag as well
        concert_title = concert.find('span', attrs={'class': 'event-title'}).getText().strip()
        concert_date = parse_date(concert.find('span', attrs={'class': 'event-date'}).getText().strip())
        concert_url = BASE_URL + concert.get('href')
        concerts.append(
            Concert(concert_title, concert_date, venue.name, concert_url)
        )

    logger.info(f"Found {len(concerts)} concerts for venue {venue.name}")
    return concerts
