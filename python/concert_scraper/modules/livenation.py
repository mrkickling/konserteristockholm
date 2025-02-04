"""Fetch data from livenation.se"""
from datetime import datetime

from bs4 import BeautifulSoup

from ..common import Concert
from ..logger import get_logger

logger = get_logger(__name__)
BASE_URL = "https://livenation.se"


def parse_date(concert_day, concert_month_year):
    # custom short month format for livenation
    months_se = [
        "jan", "feb", "mars", "apr", "maj", "juni", "juli", "aug", "sep", "okt", "nov", "dec"
    ]
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

        concert_day_elem = concert_element.find('span', attrs={'class': 'date__day'})
        concert_day = concert_day_elem.getText() if concert_day_elem else None
        concert_month_year_elem = concert_element.find('span', attrs={'class': 'date__month'})
        concert_month_year = concert_month_year_elem.getText() if concert_month_year_elem else None
        concert_url = concert_element.find('a').get('href')

        if concert_day and concert_month_year:
            concert_date = parse_date(concert_day, concert_month_year)
            concerts.append(
                Concert(concert_title, concert_date, venue.name, concert_url)
            )
    logger.info(f"Found {len(concerts)} concerts for venue {venue.name}")
    return concerts
