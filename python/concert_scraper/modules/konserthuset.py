"""Fetch data from konserthuset.se"""

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time
from datetime import datetime

from concert_scraper.common import Concert
from concert_scraper.logger import get_logger

logger = get_logger(__name__)

BASE_URL = "https://konserthuset.se"

def parse_date(date_string):
    # 'Fredag 5 januari 2024 kl 17.00'
    months_se = [
        "januari",
        "februari",
        "mars",
        "april",
        "maj",
        "juni",
        "juli",
        "augusti",
        "september",
        "oktober",
        "november",
        "december"
    ]
    weekday, date, month, year, _, time = date_string.split()
    date_int = int(date)
    month_int = months_se.index(month.lower()) + 1
    year_int = int(year)
    return datetime(year_int, month_int, date_int).strftime("%Y-%m-%d")

def get_concerts(venue, browser):
    logger.info(f"Getting concerts for venue {venue.name}")
    browser.get(venue.url)

    time.sleep(1)
    popup = browser.find_element(By.CLASS_NAME, 'cookie-popup')
    browser.execute_script("""
    var element = arguments[0];
    element.parentNode.removeChild(element);
    """, popup)
    list_view = browser.find_element(By.CLASS_NAME, "button-detaild-view")
    list_view.click()
    time.sleep(5)
    load_all = browser.find_element(By.CLASS_NAME, "button-loadmore")
    load_all.click()
    time.sleep(8)

    html = browser.page_source

    soup = BeautifulSoup(html, features="html.parser")
    cards = soup.find_all(name="li", attrs={'class': 'jsArrangementItem'})
    concerts = []
    for card in cards:
        concert_title = card.find('h4').getText().strip()
        concert_date = parse_date(card.find('h3').getText().strip())
        concert_url = card.find('a', attrs={'class': 'hall-link'}).getText().strip()
        concerts.append(
            Concert(concert_title, concert_date, venue.name, concert_url)
        )

    logger.info(f"Found {len(concerts)} concerts for venue {venue.name}")
    return concerts
