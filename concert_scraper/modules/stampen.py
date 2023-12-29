"""Fetch data from glenmillercafe.se"""

from bs4 import BeautifulSoup
from concert_scraper.common import Concert

BASE_URL = "https://stampen.se"


def get_concerts(venue, browser):
    browser.get(venue.url)
    html = browser.page_source

    soup = BeautifulSoup(html, features="html.parser")
    cards = soup.find_all(name="article", attrs={'class': 'mec-event-article'})
    concerts = set()
    for card in cards:
        concert_title = card.find('h4', attrs={'class': 'mec-event-titlee'}).getText().strip()
        concert_date = card.find('span', attrs={'class': 'mec-event-d'}).getText().strip()
        concert_url = BASE_URL
        concerts.add(
            Concert(concert_title, concert_date, venue.name, concert_url)
        )

    return concerts
