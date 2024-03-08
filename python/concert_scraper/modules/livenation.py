"""Fetch data from livenation.se"""

from bs4 import BeautifulSoup
from datetime import datetime
from concert_scraper.common import Concert
from concert_scraper.logger import get_logger

logger = get_logger(__name__)

BASE_URL = "https://livenation.se"


def parse_date(concert_day, concert_month_year):
    months_se = ["jan", "feb", "mars", "apr", "maj", "juni", "juli", "aug", "sep", "okt", "nov", "dec"]

    month, year = concert_month_year.split(" ")
    year_int = int(year)
    month_int = months_se.index(month.rstrip(".")) + 1
    day_int = int(concert_day)

    return datetime(year_int, month_int, day_int).strftime("%Y-%m-%d")


def get_concerts(venue, browser):
    logger.info(f"Getting concerts for venue {venue.name}")
    browser.get(venue.url)
    html = browser.page_source

    soup = BeautifulSoup(html, features="html.parser")
    concert_elements = soup.find_all(name="li", attrs={'class': 'artistticket'})
    concerts = []
    for concert_element in concert_elements:
        concert_title = concert_element.find('span', attrs={'class': 'artistticket__name'}).getText()

        concert_day = concert_element.find('span', attrs={'class': 'date__day'}).getText()
        concert_month_year = concert_element.find('span', attrs={'class': 'date__month'}).getText()
        concert_url = concert_element.find('a').get('href')

        concert_date = parse_date(concert_day, concert_month_year)
        concerts.append(
            Concert(concert_title, concert_date, venue.name, concert_url)
        )
    logger.info(f"Found {len(concerts)} concerts for venue {venue.name}")
    return concerts
