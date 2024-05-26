import os
import yaml
from selenium import webdriver
from datetime import datetime, timedelta

from concert_scraper.common import Venue
from concert_scraper.exporter import export_concerts
from concert_scraper.logger import get_logger
from concert_scraper.modules import (
    nortic,
    tickster,
    glenmiller,
    stampen,
    billetto,
    scala,
    konserthuset,
    folkparken,
    fryshuset,
    geronimosfgt,
    norrport,
    gamlaenskedebryggeri,
    lykkelive,
    riche,
    facebook_events,
    livenation,
    fallan,
    cirkus
)

logger = get_logger(__name__)


def filter_concerts_by_date(concerts, max_date):
    """From a list of Concerts, return only the ones before max_date"""
    return [
        concert for concert in concerts
        if datetime.strptime(concert.date, '%Y-%m-%d') <= max_date
    ]


def shorten_titles(concerts, max_len):
    for concert in concerts:
        concert.title = concert.title[:max_len]


def scrape_venues(venues):
    """
    Using list of venues, scrape each with respective module
    @return list[Concert]
    """
    # Create the selenium browser
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    browser = webdriver.Firefox(options=options)

    concerts = []
    successful_venues = []
    failed_venues = []

    for venue in venues:
        try:
            if venue.type == "nortic":
                concerts += nortic.get_concerts(venue=venue, browser=browser)
            elif venue.type == "tickster":
                concerts += tickster.get_concerts(venue=venue, browser=browser)
            elif venue.type == "glenmiller":
                concerts += glenmiller.get_concerts(venue=venue, browser=browser)
            elif venue.type == "stampen":
                concerts += stampen.get_concerts(venue=venue, browser=browser)
            elif venue.type == "billetto":
                concerts += billetto.get_concerts(venue=venue, browser=browser)
            elif venue.type == "scala":
                concerts += scala.get_concerts(venue=venue, browser=browser)
            elif venue.type == "konserthuset":
                concerts += konserthuset.get_concerts(venue=venue, browser=browser)
            elif venue.type == "folkparken":
                concerts += folkparken.get_concerts(venue=venue, browser=browser)
            elif venue.type == "fryshuset":
                concerts += fryshuset.get_concerts(venue=venue, browser=browser)
            elif venue.type == "geronimosfgt":
                concerts += geronimosfgt.get_concerts(venue=venue, browser=browser)
            elif venue.type == "norrport":
                concerts += norrport.get_concerts(venue=venue, browser=browser)
            elif venue.type == "gamlaenskedebryggeri":
                concerts += gamlaenskedebryggeri.get_concerts(venue=venue, browser=browser)
            elif venue.type == "lykkelive":
                concerts += lykkelive.get_concerts(venue=venue, browser=browser)
            elif venue.type == "riche":
                concerts += riche.get_concerts(venue=venue, browser=browser)
            elif venue.type == "facebook_events":
                concerts += facebook_events.get_concerts(venue=venue, browser=browser)
            elif venue.type == "livenation":
                concerts += livenation.get_concerts(venue=venue, browser=browser)
            elif venue.type == "fallan":
                concerts += fallan.get_concerts(venue=venue, browser=browser)
            elif venue.type == "cirkus":
                concerts += cirkus.get_concerts(venue=venue, browser=browser)
            else:
                continue
            successful_venues.append(venue.name)
        except Exception as e:
            failed_venues.append(venue.name)
            logger.error(f"Failed to scrape {venue.name} - {e}")

    browser.quit()
    return concerts, successful_venues, failed_venues


def get_all_venues():
    """Read yaml file with venues, return as list[Venue]"""
    yaml_path = os.path.join(os.path.dirname(__file__), 'conf/venues.yml')
    venues_yml = yaml.safe_load(open(yaml_path))
    return [
        Venue(
            venue['title'],
            venue['address'],
            venue['type'],
            venue['url'],
            venue.get('filter_keywords', [])
        ) for venue in venues_yml.values()]


def main():
    if not os.getenv('api_url') or not os.getenv('api_key'):
        raise Exception("Remember to set your envs!")

    # Scrape all venues for concerts
    logger.info("Starting the scraper")
    venues = get_all_venues()
    concerts, successful_venues, failed_venues = scrape_venues(venues)
    logger.info(f"Found {len(concerts)} concerts in total")

    # Only care about concerts within 10 months in the future
    # This avoids bug where we add concerts 1 year into the future that
    # already just took place.
    # TODO: Handle bug in a better way so we don't miss actual future concerts.
    date_in_future = datetime.now() + timedelta(10 * 30)
    concerts = filter_concerts_by_date(concerts, date_in_future)
    shorten_titles(concerts, 254)

    # Export to api
    export_concerts(concerts, successful_venues, failed_venues)
