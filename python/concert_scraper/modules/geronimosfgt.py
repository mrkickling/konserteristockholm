# https://www.geronimosfgt.se/shows-events-live-music/
from bs4 import BeautifulSoup
from concert_scraper.common import Concert
from datetime import datetime, timedelta
from concert_scraper.logger import get_logger

logger = get_logger(__name__)

BASE_URL = "https://www.geronimosfgt.se/shows-events-live-music"

def parse_date(date_string):
    date_info = date_string.split('-')
    month = date_info[-1].split().pop(-1)
    raw_dates = "".join(date_info).split()[:-1]
    months_se = ["jan", "feb", "mar", "apr", "maj", "jun", "jul", "aug", "sep", "okt", "nov", "dec"]

    dates = []
    month_int = months_se.index(month) + 1
    for date in raw_dates:
        day_int = int(date)
        date = datetime(1904, month_int, day_int)
        now = datetime.now()
        try:
            date = date.replace(year=now.year)
        except ValueError:
            # Handle feb 29th
            date = date.replace(year=now.year + 1)
        if date < now - timedelta(1):
            date = date.replace(year=now.year + 1)
        dates.append(date.strftime("%Y-%m-%d"))
    return dates


def get_concerts(venue, browser):
    logger.info(f"Getting concerts for venue {venue.name}")
    browser.get(venue.url)
    html = browser.page_source

    soup = BeautifulSoup(html, features="html.parser")
    cards = soup.find_all(name="div", attrs={'class': 'mec-topsec'})
    concerts = []
    for card in cards:
        card = card.parent()[0]
        concert_title = card.find('h3').getText().strip()
        concert_dates = parse_date(card.find('span', attrs={'class': 'mec-event-d'}).getText())
        concert_url = card.find('a').get('href')
        for concert_date in concert_dates:
            concerts.append(
                Concert(concert_title, concert_date, venue.name, concert_url)
            )

    logger.info(f"Found {len(concerts)} concerts for venue {venue.name}")
    return concerts
