"""Fetch data from livenation.se"""
from datetime import datetime

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from ..common import Concert
from ..logger import get_logger

logger = get_logger(__name__)
BASE_URL = "https://livenation.se"


def parse_date(date_string):
    """2025-04-02T:00:00:00.000Z"""
    return date_string[:10]


def get_concerts(venue, browser):
    logger.info(f"Getting concerts for venue {venue.name}")
    browser.get(venue.url)

    xpath = "/html/body/div/main/div/div/div/section/section/ul/li/a/div"
    concert_elements = browser.find_elements(By.XPATH, xpath)
    concerts = []

    for concert_element in concert_elements:
        concert_date_elem = concert_element.find_element(By.CSS_SELECTOR, "time")
        concert_date = parse_date(concert_date_elem.get_attribute('datetime'))
        concert_title = concert_element.find_element(By.CSS_SELECTOR, "h4").text
        concert_url = concert_element.find_element(By.XPATH, '..').get_attribute('href')
        concerts.append(
            Concert(concert_title, concert_date, venue.name, concert_url)
        )
    logger.info(f"Found {len(concerts)} concerts for venue {venue.name}")
    return concerts
