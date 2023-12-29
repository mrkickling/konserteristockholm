"""Fetch data from glenmillercafe.se"""

from bs4 import BeautifulSoup
from concert_scraper.common import Concert
from datetime import datetime

BASE_URL = "https://glenmillercafe.se"

def parse_date(date_string):
    return datetime.strptime(date_string, '%Y-%m-%d')

def get_concerts(venue, browser):
    browser.get(venue.url)
    html = browser.page_source

    soup = BeautifulSoup(html, features="html.parser")
    cards = soup.find_all(name="div", attrs={'class': 'konsert'})
    concerts = set()
    for card in cards:
        concert_title = card.find('p', attrs={'class': 'artist'}).getText()
        concert_date = parse_date(card.find('p', attrs={'class': 'date'}).getText())
        concert_url = BASE_URL
        concerts.add(
            Concert(concert_title, concert_date, venue.name, concert_url)
        )

    return concerts
