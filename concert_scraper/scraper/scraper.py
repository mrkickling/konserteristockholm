from selenium import webdriver

from modules import nortic, tickster, glenmiller, stampen, billetto, scala, konserthuset
from common import Venue

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
        "Townhouse Nouch & Chow",
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
        "Glen Miller Café Konserter",
        "Brunnsgatan 21A",
        "glenmiller",
        "https://www.glennmillercafe.se/konserter"
    ),
    Venue(
        "Glen Miller Café Klassiska Konserter",
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
        "Konserthuset",
        "Hötorget",
        "konserthuset",
        "https://www.konserthuset.se/program-och-biljetter/kalender/"
    )
]

options = webdriver.FirefoxOptions()
browser = webdriver.Firefox(options=options)
concerts = set()

for venue in venues:
    if venue.type == "nortic":
        concerts = concerts.union(
            nortic.get_concerts(venue=venue, browser=browser))
    elif venue.type == "tickster":
        concerts = concerts.union(
            tickster.get_concerts(venue=venue, browser=browser))
    elif venue.type == "glenmiller":
        concerts = concerts.union(
            glenmiller.get_concerts(venue=venue, browser=browser))
    elif venue.type == "stampen":
        concerts = concerts.union(
            stampen.get_concerts(venue=venue, browser=browser))
    elif venue.type == "billetto":
        concerts = concerts.union(
            billetto.get_concerts(venue=venue, browser=browser))
    elif venue.type == "scala":
        concerts = concerts.union(
            scala.get_concerts(venue=venue, browser=browser))
    elif venue.type == "konserthuset":
        concerts = concerts.union(
            konserthuset.get_concerts(venue=venue, browser=browser))

for concert in concerts:
    print(concert)

browser.quit()
