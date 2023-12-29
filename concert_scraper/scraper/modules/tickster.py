"""Fetch data from tickster.com"""

from bs4 import BeautifulSoup
from common import Concert

BASE_URL = "https://tickster.com"


def get_concerts(venue, browser):
    browser.get(venue.url)
    html = browser.page_source

    def clean_date(date_str):
        dates = date_str.split(",")
        start_date = dates[0].strip()
        return start_date

    soup = BeautifulSoup(html, features="html.parser")
    cards = soup.find_all(name="div", attrs={'class': 'c-tile'})
    concerts = set()
    for card in cards:
        concert_title = card.find('h2').getText().strip()
        date_attrs = {'class': 'c-tile__label'}
        concert_date = clean_date(
            card.find('span', attrs=date_attrs).getText())
        concert_url = BASE_URL + card.find('a').get('href')
        concerts.add(
            Concert(concert_title, concert_date, venue.name, concert_url)
        )

    return concerts
