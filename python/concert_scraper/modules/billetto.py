"""Fetch data from billetto.se"""

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from datetime import datetime

from concert_scraper.common import Concert, get_future_date
from concert_scraper.logger import get_logger

logger = get_logger(__name__)

BASE_URL = "https://billetto.se"

def parse_date(date_string):
    """ Convert the format from billetto to a datetime object """
    # date month. hour:minute or date month hour:minute
    months_se = [
        "jan", "feb", "mars", "apr", "maj", "juni", "juli", "aug", "sep", "okt", "nov", "dec"
    ]
    day, month, time = date_string.split()
    month_int = months_se.index(month.rstrip('.')) + 1
    day_int = int(day)
    date = get_future_date(month_int, day_int)

    return date.strftime("%Y-%m-%d")

def get_concerts(venue, browser):
    logger.info(f"Getting concerts for venue {venue.name}")
    browser.get(venue.url)
    time.sleep(5)
    concerts = []

    try:
        cookie_button = browser.find_element(By.ID, "onetrust-accept-btn-handler")
        cookie_button.click()
    except NoSuchElementException:
        logger.info("No cookie banner")

    time.sleep(1)

    while True:
        # Go through all pages
        html = browser.page_source

        def clean_date(date_str):
            dates = date_str.split("-")
            start_date = dates[0].strip()
            return start_date

        soup = BeautifulSoup(html, features="html.parser")

        # Sadly the elements can not be identified except for their combination of classes
        classes = "bg-white dark:bg-gray-800 flex flex-col justify-between relative border-gray-200 dark:border-gray-700 sm:rounded-lg divide-y divide-gray-200 dark:divide-gray-700 border shadow overflow-hidden"
        concert_elements = soup.find_all(name="div", attrs={'class': classes})
        for concert in concert_elements:
            title_attrs = {'class': 'block text-white hover:text-brand-500 font-medium text-base truncate'}
            concert_title = concert.find('a', attrs=title_attrs)
            if not concert_title or not len(concert_title.getText()):
                continue
            concert_title = concert_title.getText()

            date_attrs = {'class': 'border border-gray-200 p-1 text-xs text-brand-500 bg-white rounded-md'}
            concert_date = clean_date(concert.find(attrs=date_attrs).get_text())
            concert_date = parse_date(concert_date)

            concert_url = concert.find('a').get('href') if concert.find('a') else venue.url
            concerts.append(
                Concert(concert_title, concert_date, venue.name, concert_url)
            )

        # Next page
        try:
            button = browser.find_element(By.CSS_SELECTOR, "[aria-label=Nästa]")
            if button.is_enabled():
                button.click()
            else:
                break
        except NoSuchElementException:
            break

    logger.info(f"Found {len(concerts)} concerts for venue {venue.name}")
    return concerts
