"""Fetch data from glenmillercafe.se"""

from selenium.webdriver.common.by import By
from datetime import datetime
from bs4 import BeautifulSoup
import time

from concert_scraper.common import Concert

BASE_URL = "https://www.scalateatern.se/forestallningar/"

def parse_date(date_string):
    # 5 jan
    months_se = ["jan", "feb", "mar", "apr", "maj", "jun", "jul", "aug", "sep", "okt", "nov", "dec"]
    day, month = date_string.split()
    month_int = months_se.index(month) + 1
    day_int = int(day)
    date = datetime(1904, month_int, day_int)
    now = datetime.now()
    try:
        date = date.replace(year=now.year)
    except ValueError:
        # Handle feb 29th
        date = date.replace(year=now.year + 1)
    if date < now:
        date = date.replace(year=now.year + 1)
    return date

def get_concerts(venue, browser):
    browser.get(venue.url)

    # 'Load more' as many times as possible
    time.sleep(2)
    button = browser.find_element(By.CLASS_NAME, "post-list-load-more")
    while button.is_displayed():
        print("Load more")
        button.click()
        time.sleep(2)

    html = browser.page_source

    soup = BeautifulSoup(html, features="html.parser")
    cards = soup.find_all(attrs={'class': 'post-list--item'})
    concerts = set()
    for card in cards:
        concert_title = card.find(attrs={'class': 'title d-block text-uppercase text-bold'}).getText().strip()
        day = card.find(attrs={'class': 'day'}).getText().strip()
        month = card.find(attrs={'class': 'month'}).getText().strip()
        concert_url = card.find('a').get('href')
        genre = card.find('div', attrs={'class':'meta'}).findAll('span')[-1].getText().strip()
        if genre == "Musik":
            concerts.add(
                Concert(concert_title, parse_date(day + " " + month), venue.name, concert_url)
            )

    return concerts
