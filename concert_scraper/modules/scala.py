"""Fetch data from glenmillercafe.se"""

from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

from concert_scraper.common import Concert

BASE_URL = "https://www.scalateatern.se/forestallningar/"


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
                Concert(concert_title, day + " " + month, venue.name, concert_url)
            )

    return concerts
