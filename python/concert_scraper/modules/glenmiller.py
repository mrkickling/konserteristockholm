"""Fetch data from https://www.glennmillercafe.se"""

from datetime import datetime

from selenium.webdriver.common.by import By

from ..common import Concert
from ..logger import get_logger

logger = get_logger(__name__)
BASE_URL = "https://www.glennmillercafe.se"

def parse_date(date_string):
    return datetime.strptime(date_string, '%Y-%m-%d').strftime("%Y-%m-%d")

def get_concerts(venue, browser):
    logger.info(f"Getting concerts for venue {venue.name}")
    browser.get(venue.url)
    xpath = "/html/body/div/div/div/div/main/div/div/div/div/div/div/div/section/div/div/section/div/div/div/div/div/div/div"
    concert_elements = browser.find_elements(By.XPATH, xpath)
    concerts = []

    for concert in concert_elements:
        meta = concert.text.split("\n")
        artist = "".join(meta[0:-1]) # All before last element is artist
        try:
            date = parse_date(meta[-1]) # Last element is date
        except:
            logger.error("Failed to parse date %s", meta[-1])
            continue
        concert_url = venue.url

        concerts.append(
            Concert(artist, date, venue.name, concert_url)
        )

    logger.info(f"Found {len(concerts)} concerts for venue {venue.name}")
    return concerts
