"""Fetch data from https://www.glennmillercafe.se"""

from bs4 import BeautifulSoup
from concert_scraper.common import Concert
from datetime import datetime
from concert_scraper.logger import get_logger

logger = get_logger(__name__)

BASE_URL = "https://www.lykkelive.com/concerts/"

def parse_date(date_string):
    date_string = date_string[-10:] # Date assumed to be 10 digits
    return datetime.strptime(date_string, '%Y-%m-%d').strftime("%Y-%m-%d")

def get_concerts(venue, browser):
    logger.info(f"Getting concerts for venue {venue.name}")
    browser.get(venue.url)
    html = browser.page_source

    soup = BeautifulSoup(html, features="html.parser")

    cards = soup.find_all("div", attrs={'class': 'concerts__page'})
    concerts = []
    for card in cards:
        concert_title = card.find('h2').getText()
        concert_date = parse_date(card.find('div', attrs={'class': 'concert__dates'}).getText())
        concert_url = venue.url
        concerts.append(
            Concert(concert_title, concert_date, venue.name, concert_url)
        )

    logger.info(f"Found {len(concerts)} concerts for venue {venue.name}")
    return concerts
