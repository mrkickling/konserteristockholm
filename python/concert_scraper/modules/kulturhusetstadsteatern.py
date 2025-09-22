# https://kulturhusetstadsteatern.se/kalender?category=3
import time
import datetime

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from ..common import Concert, get_future_date
from ..logger import get_logger
from .utils import months_se

logger = get_logger(__name__)
BASE_URL = "https://kulturhusetstadsteatern.se/konserter/"


def parse_date(date_string):
    """23 september, kl 12:00"""

    if date_string == "IDAG":
        return datetime.datetime.today().strftime("%Y-%m-%d")
    if date_string == "IMORGON":
        return (
            datetime.datetime.today() + datetime.timedelta(1)
        ).strftime("%Y-%m-%d")

    day, month, *_ = date_string.split()
    month = month.removesuffix(',')
    month_int = months_se.index(month.lower()) + 1
    day_int = int(day)
    date = get_future_date(month_int, day_int)
    return date.strftime("%Y-%m-%d")


def get_concerts(venue, browser):
    logger.info("Getting concerts for venue %s", venue.name)
    browser.get(venue.url)

    time.sleep(1)
    try:
        cookie_button = browser.find_element(By.XPATH, "//*[contains(text(), 'Godkänn')]")
        cookie_button.click()
    except NoSuchElementException:
        logger.info("Found no cookie popup - weird?")

    while True:
        try:
            load_all = browser.find_element(
                By.CSS_SELECTOR, ".calendar-filter__load-more"
            )
            load_all.click()
            time.sleep(0.5)
        except NoSuchElementException:
            break

    html = browser.page_source
    soup = BeautifulSoup(html, features="html.parser")
    cards = soup.find_all(name="li", attrs={'class': 'single-result'})
    concerts = []

    for card in cards:
        concert_title = card.find('h3').getText().strip()
        concert_date_obj = card.find(
            name='p', attrs={'class': 'single-result__dates'}
        )
        if concert_date_obj:
            last_seen_date = parse_date(concert_date_obj.getText().strip())
            concert_url = card.find('a').get('href')
            concerts.append(
                Concert(concert_title, last_seen_date, venue.name, concert_url)
            )

    logger.info(f"Found {len(concerts)} concerts for venue {venue.name}")
    return concerts
