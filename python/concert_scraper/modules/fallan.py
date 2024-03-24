"""Module for venue Fållan"""
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import re
from datetime import datetime

from concert_scraper.common import Concert, get_future_date
from concert_scraper.logger import get_logger


logger = get_logger(__name__)
BASE_URL = "https://www.fallan.nu/whats-on"


def parse_date(date_string):
    """Convert from Fållan format"""
    # Oct 11, 2024
    date = datetime.strptime(date_string.capitalize(), "%b %d, %Y")
    return date.strftime("%Y-%m-%d")


def get_concerts(venue, browser):
    logger.info(f"Getting concerts for venue {venue.name}")
    browser.get(venue.url)

    concerts = []
    time.sleep(1)
    try:
        cookie_button = browser.find_element(
            By.ID,
            "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"
        )
        cookie_button.click()
    except NoSuchElementException:
        logger.info("No cookie banner")

    # Scroll to bottom
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    html = browser.page_source
    soup = BeautifulSoup(html, features="html.parser")

    # All concert sections have the class event-card-2
    concert_elements = soup.find_all("section", attrs={'class': 'event-card-2'})
    for concert in concert_elements:
        try:
            concert_title = concert.find('h4').getText()
            concert_date = parse_date(concert.find('h2').getText())
            concert_url = concert.find('a').get('href') if concert.find('a') else venue.url

            concerts.append(
                Concert(concert_title, concert_date, venue.name, concert_url)
            )
        except ValueError:
            logger.error("Failed to add concert")

    logger.info(f"Found {len(concerts)} concerts for venue {venue.name}")
    return concerts
