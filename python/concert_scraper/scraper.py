import os
from selenium import webdriver
from datetime import datetime, timedelta

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
    folkparken,
    gamlaenskedebryggeri,
    lykkelive,
    riche,
    facebook_events,
    livenation
)
from concert_scraper.common import Venue
from concert_scraper.logger import get_logger
from concert_scraper.exporter import export_concerts

logger = get_logger(__name__)

venues = [
    Venue(
        "Fasching",
        "Norrmalm",
        "nortic",
        "https://www.nortic.se/ticket/organizer/3020"
    ),
    Venue(
        "Reimersholme Hotell",
        "Reimersholme",
        "tickster",
        "https://www.tickster.com/sv/events/at/7hpytvme5t7htay/reimersholme-hotel?take=100?take=100"
    ),
    Venue(
        "Kollektivet Livet Bar & Scen",
        "Stadsgårdsterminalen",
        "tickster",
        "https://www.tickster.com/sv/events/at/hd7g2z5jf75bvcj/kollektivet-livet-bar-and-scen?take=100"
    ),
    Venue(
        "Townhouse Nosh & Chow",
        "Norrlandsgatan 24, Stockholm",
        "tickster",
        "https://www.tickster.com/sv/events/at/h8l6zral0kx2y5b/townhouse-nosh-and-chow?take=100"
    ),
    Venue(
        "Biblioteket Live",
        "Medborgarplatsen",
        "tickster",
        "https://www.tickster.com/sv/events/at/2nkerrp3y8re7l0/biblioteket-live?take=100"
    ),
    Venue(
        "Debaser Strand",
        "Honstulls Strand 4",
        "tickster",
        "https://www.tickster.com/sv/events/at/c3y3dpad56ncfp4/debaser-strand?take=100"
    ),
    Venue(
        "Nalen Klubb",
        "David Bagares Gata 15",
        "tickster",
        "https://www.tickster.com/sv/events/at/103c9wa31d3j16b/nalen-klubb-stockholm?take=100"
    ),
    Venue(
        "Kägelbanan Södra Teatern",
        "Mosebacke Torg 1",
        "tickster",
        "https://www.tickster.com/sv/events/at/16akr7hjdhpd4nv/kagelbanan-sodra-teatern?take=100"
    ),
    Venue(
        "Bar Brooklyn",
        "Hornstulls Strand 4",
        "tickster",
        "https://www.tickster.com/sv/events/at/rmvdctd43351vpf/bar-brooklyn?take=100"
    ),
    Venue(
        "Södra Teaterns Stora Scen",
        "Mosebacke Torg 1",
        "tickster",
        "https://www.tickster.com/sv/events/at/w99v7b6udfhj2gw/sodra-teaterns-stora-scen?take=100"
    ),
    Venue(
        "Konstakademien",
        "Fredsgatan 12",
        "tickster",
        "https://www.tickster.com/sv/events/at/7lplt0z7ft2b2pj/konstakademien?take=100"
    ),
    Venue(
        "Under Bron",
        "Hammarby Slussväg 2",
        "tickster",
        "https://www.tickster.com/sv/events/at/hxhmufbv2c62wa5/under-bron?take=100"
    ),
    Venue(
        "Trädgården",
        "Hammarby Slussväg 2",
        "tickster",
        "https://www.tickster.com/sv/events/at/2uzz6tlz8z8x2f4/tradgarden?take=100"
    ),
    Venue(
        "Glenn Miller Café Konserter",
        "Brunnsgatan 21A",
        "glenmiller",
        "https://www.glennmillercafe.se/konserter"
    ),
    Venue(
        "Glenn Miller Café Klassiska Konserter",
        "Brunnsgatan 21A",
        "glenmiller",
        "https://www.glennmillercafe.se/klassiska-konserter"
    ),
    Venue(
        "Stampen",
        "Stora Gråmunkegränd 7",
        "stampen",
        "https://www.stampen.se/program/"
    ),
    Venue(
        "Slaktkyrkan, Johanneshov",
        "Slakthusområdet",
        "billetto",
        "https://billetto.se/users/slaktkyrkan-hus-7"
    ),
    Venue(
        "Scalateatern",
        "Scalateatern",
        "scala",
        "https://www.scalateatern.se/forestallningar/"
    ),
    Venue(
        "Norrport",
        "Roslagsgatan 38",
        "norrport",
        "https://norrport.se/evenemang/"
    ),
    Venue(
        "Fryshuset",
        "Hammarby Sjöstad",
        "fryshuset",
        "https://fryshuset.se/konserter/",
    ),
    Venue(
        "Geronimo's FGT",
        "Gamla Stan",
        "geronimosfgt",
        "https://www.geronimosfgt.se/shows-events-live-music/"
    ),
    Venue(
        "Gamla Enskede Bryggeri",
        "Bolidenvägen 8",
        "gamlaenskedebryggeri",
        "https://gamlaenskedebryggeri.se/pa-gang/"
    ),
    Venue(
        "Lykke Live",
        "Nytorgsgatan 38",
        "lykkelive",
        "https://www.lykkelive.com/concerts/"
    ),
    Venue(
        "Riche / Lilla baren",
        "Birger Jarlsgatan 4",
        "riche",
        "https://riche.se/kalendarium"
    ),
    Venue(
        "Landet",
        "Hägersten",
        "billetto",
        "https://billetto.se/users/landet-telefonplan"
    ),
    Venue(
        "Gröna Lund",
        "Djurgården",
        "facebook_events",
        "https://www.facebook.com/gronalundstivoli/events"
    ),
    Venue(
        "Engelen",
        "Gamla Stan",
        "facebook_events",
        "https://www.facebook.com/EngelenKolingen/events" # "https://www.engelen.se/#spelningar"
    ),
    Venue(
        "Melodybox",
        "Hägersten",
        "facebook_events",
        "https://www.facebook.com/profile.php?id=100063670567136&sk=upcoming_hosted_events"
    ),
    Venue(
        "Hökarängens Antikvariat & Skivbörs",
        "Hökarängen",
        "facebook_events",
        "https://www.facebook.com/hokarangensantikvariat/upcoming_hosted_events"
    )

    # TODO: https://www.ticketmaster.se/venue/cirkus-stockholm-biljetter/cir/580
    # https://www.clubcover.se/tid-plats
    # TBA
    # Venue(
    #     "Snövit",
    #     "Ringvägen, Södermalm",
    #     "facebook",
    #     "https://www.facebook.com/profile.php?id=100064027210409&sk=events"
    #      "https://www.facebook.com/groups/120195232723/" - club probation
    # ),
    # TBA
    # Venue(
    #     "Fylkingen",
    #     "Mariatorget",
    #     "fylkingen",
    #     "http://fylkingen.se/program"
    # ),
    # TBA
    # Venue(
    #     "Scen 44",
    #     "Tjärhovsgatan",
    #     "facebook",
    #     "https://www.facebook.com/profile.php?id=100057341804866&sk=events"
    # ),
    # TBA
    # Venue(
    #     "Folkparken",
    #     "Sveavägen 53",
    #     "folkparken",
    #     "https://restaurangfolkparken.se/pa-scen/"
    # ),
    # TBA
    # Venue(
    #     "The Node",
    #     "Sergels Torg",
    #     "thenode",
    #     "https://thenode.se/kalendarium"
    # ),
    
    
    # Venue(
    #     "St:a Clara",
    #     "Gamla Stan",
    #     "staclara",
    #     "https://staclara.se/bierhus%201/musik%20schema"
    #     "https://www.facebook.com/pages/StA-Clara-Bierhaus/247605358698574" # finns även på facebook
    # ),
    # Venue(
    #     "Stockholm Under Stjärnorna",
    #     "Brunkebergstorg",
    #     "ticketmaster",
    #     "https://www.ticketmaster.se/venue/stockholm-under-stjarnorna-stockholm-biljetter/t3k/632"
    # ),
    # Venue(
    #     "Taverna Brillo",
    #     "Olika platser",
    #     "tavernabrillo",
    #     "https://tavernabrillo.se/kalendarium/"
    # ),
    # Inget intressant här
    # Venue(
    #     "Cyklopen",
    #     "Högdalen",
    #     "cyklopen",
    #     "https://cyklopen.se/kalender/action~agenda/request_format~json/tag_ids~60/"
    # ),
    # TBA
    # Venue(
    #     "Fållan",
    #     "Slakthusområdet",
    #     "fallan",
    #     "https://www.fallan.nu/"
    # ),
    # Venue(
    #     "Konserthuset",
    #     "Hötorget",
    #     "konserthuset",
    #     "https://www.konserthuset.se/program-och-biljetter/kalender/"
    # )
    # Venue(
    #     "Broder Tuck",
    #     "Götgatan",
    #     "zippertic",
    #     "https://api.zippertic.se/api/events?promoter=3133&passed=0" # Fel
    #     "https://www.facebook.com/pages/Broder-Tuck/168010629909374"
    # ),
]

def filter_concerts_by_date(concerts, max_date):
    return [
        concert for concert in concerts
        if datetime.strptime(concert.date, '%Y-%m-%d') <= max_date
    ]

def main():
    if not os.getenv('api_url') or not os.getenv('api_key'):
        raise Exception("Remember to set your envs!")

    logger.info("Starting the scraper")
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    browser = webdriver.Firefox(options=options)
    concerts = []

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
            elif venue.type == "folkparken":
                concerts += folkparken.get_concerts(venue=venue, browser=browser)
            elif venue.type == "lykkelive":
                concerts += lykkelive.get_concerts(venue=venue, browser=browser)
            elif venue.type == "riche":
                concerts += riche.get_concerts(venue=venue, browser=browser)
            elif venue.type == "facebook_events":
                concerts += facebook_events.get_concerts(venue=venue, browser=browser)
        except Exception as e:
            logger.error(f"Failed to scrape {venue.name} - {e}")

    logger.info(f"Found {len(concerts)} concerts in total")
    browser.quit()
    # Only care about concerts within 8 months in the future
    # This avoids bug where we add concerts 1 year into the future that
    # already took place
    date_in_half_year = datetime.now() + timedelta(8 * 30)
    concerts = filter_concerts_by_date(concerts, date_in_half_year)
    export_concerts(concerts)
