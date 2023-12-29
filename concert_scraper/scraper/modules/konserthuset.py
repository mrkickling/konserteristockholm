"""Fetch data from glenmillercafe.se"""

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time

from common import Concert

BASE_URL = "https://konserthuset.se"


def get_concerts(venue, browser):
    browser.get(venue.url)

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
    concerts = set()
    for card in cards:
        concert_title = card.find('h4').getText().strip()
        concert_dates = card.find('h3').getText().strip()
        concert_url = card.find('a', attrs={'class': 'hall-link'}).getText().strip()
        concerts.add(
            Concert(concert_title, concert_dates, venue.name, concert_url)
        )

    return concerts
