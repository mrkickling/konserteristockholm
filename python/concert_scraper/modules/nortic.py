"""Fetch data from nortic.se"""

from bs4 import BeautifulSoup
from datetime import datetime
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from concert_scraper.common import Concert
from concert_scraper.logger import get_logger

logger = get_logger(__name__)

BASE_URL = "https://nortic.se"


def parse_date(date_string):
    # 5 January
    # Need to use a leap year as default otherwise we crash from feb 29th
    date = datetime.strptime(f"1904 {date_string}", '%Y %d %B')
    now = datetime.now()
    try:
        date = date.replace(year=now.year)
    except ValueError:
        print("Failed to parse date - trying with next year instead")
    if date < now:
        date = date.replace(year=now.year+1)
    return date

def get_concerts(venue, browser):
    logger.info(f"Getting concerts for venue {venue.name}")
    browser.get(venue.url)
    check = EC.presence_of_element_located((By.ID, 'event-card-grid'))
    WebDriverWait(browser, 5).until(check)
    html = browser.page_source

    def clean_date(date_str):
        dates = date_str.split("-")
        start_date = dates[0].strip()
        return start_date

    soup = BeautifulSoup(html, features="html.parser")
    cards = soup.find_all(name="div", attrs={'class': 'card'})
    concerts = set()
    for card in cards:
        concert_title = card.find(name="h3").text
        date_attrs = {'class': 'time'}
        concert_date = parse_date(clean_date(card.find(attrs=date_attrs).get_text()))
        concert_url = BASE_URL + card.find('a').get('href')
        concerts.add(
            Concert(concert_title, concert_date, venue.name, concert_url)
        )
    logger.info(f"Found {len(concerts)} concerts for venue {venue.name}")
    return concerts
