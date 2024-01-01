# https://gamlaenskedebryggeri.se/pa-gang/

from bs4 import BeautifulSoup
from concert_scraper.common import Concert
from datetime import datetime
import re
from concert_scraper.logger import get_logger

logger = get_logger(__name__)

BASE_URL = "https://www.gamlaenskedebryggeri.se"

def parse_date(date_string):
    # 13/12
    day, month = date_string.split('/')
    day_int = int(day)
    month_int = int(month)
    date = datetime(1904, month_int, day_int)
    now = datetime.now()
    try:
        date = date.replace(year=now.year)
    except ValueError:
        # Handle feb 29th
        date = date.replace(year=now.year + 1)
    if date < now:
        date = date.replace(year=now.year + 1)

    return date.strftime("%Y-%m-%d")

def get_concerts(venue, browser):
    logger.info(f"Getting concerts for venue {venue.name}")
    browser.get(venue.url)
    html = browser.page_source

    concerts = []
    soup = BeautifulSoup(html, features='html.parser')
    potential_concerts = soup.find_all('p')
    for potential in potential_concerts:
        text = potential.getText()
        pattern = re.compile('\d+\/\d+ .*')
        hit = pattern.match(text)
        if hit:
            concert = hit.group()
            date, *concert_title_parts = concert.split()
            concert_title = " ".join(concert_title_parts)
            concert_date = parse_date(date)
            concert_url = potential.find('a').get('href') if potential.find('a') else venue.url
            concerts.append(
                Concert(concert_title, concert_date, venue.name, concert_url)
            )

    logger.info(f"Found {len(concerts)} concerts for venue {venue.name}")
    return concerts
