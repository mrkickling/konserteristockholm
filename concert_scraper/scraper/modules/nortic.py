"""Fetch data from nortic.se"""

from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from common import Concert

BASE_URL = "https://nortic.se"


def get_concerts(venue, browser):
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
        concert_dates = clean_date(card.find(attrs=date_attrs).get_text())
        concert_url = BASE_URL + card.find('a').get('href')
        concerts.add(
            Concert(concert_title, concert_dates, venue.name, concert_url)
        )

    return concerts
