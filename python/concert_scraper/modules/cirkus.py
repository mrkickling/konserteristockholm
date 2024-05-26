"""Fetch data from livenation.se"""

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import time
from datetime import datetime
from concert_scraper.common import Concert
from concert_scraper.logger import get_logger

logger = get_logger(__name__)

BASE_URL = "https://cirkus.se"


def parse_date(concert_month, concert_day, concert_year):
    months_se = ["jan", "feb", "mar", "apr", "maj", "jun", "jul", "aug", "sep", "okt", "nov", "dec"]

    year_int = int(concert_year)
    month_int = months_se.index(concert_month.lower()) + 1
    day_int = int(concert_day)
    return datetime(year_int, month_int, day_int).strftime("%Y-%m-%d")


def get_concerts(venue, browser):
    logger.info(f"Getting concerts for venue {venue.name}")
    browser.get(venue.url)

    time.sleep(2)
    try:
        cookie_button = browser.find_element(
            By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")
        cookie_button.click()
    except NoSuchElementException:
        logger.info("No cookie banner")

    # Only show 'konserter'
    genre_button = browser.find_element(
        By.ID, "genresDropdownButton"
    )
    genre_button.click()

    konserter_checkbox = browser.find_element(
        By.CSS_SELECTOR, "div.dropdown-item:nth-child(8)"
    )
    konserter_checkbox.click()

    # Scroll to bottom a few times
    for i in range(10):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

    html = browser.page_source
    soup = BeautifulSoup(html, features="html.parser")
    concert_elements = soup.find_all("div", attrs={'class': 'single-event-item'})
    concerts = []

    for concert_element in concert_elements:
        concert_title = concert_element.find('h3', attrs={'class': 'event-bottom-wrapper-title'}).getText().strip()

        concert_month = concert_element.find('div', attrs={'class': 'event-date event-date-month'}).getText()
        concert_day = concert_element.find('div', attrs={'class': 'event-date-day'}).getText()
        concert_year = concert_element.find('div', attrs={'class': 'event-date-year'}).getText()

        concert_url = concert_element.find('a').get('href')

        concert_date = parse_date(concert_month, concert_day, concert_year)

        concerts.append(
            Concert(concert_title, concert_date, venue.name, concert_url)
        )
    
    logger.info(f"Found {len(concerts)} concerts for venue {venue.name}")
    return concerts
