from concert_scraper.common import Concert, Venue
from concert_scraper.modules.utils import filter_keywords
from concert_scraper.scraper import get_all_venues

def test_filter_keywords():
    venue = Venue(
        "Gröna Lund",
        "Stockholm",
        "?",
        "https://",
        ["inte är musik", "Ej musik"]
    )
    event1 = Concert(
        'En grej som inte är musik',
        '2024-23-24',
        'Gröna Lund',
        'https://lol'
    )
    event2 = Concert(
        'En grej som är musik',
        '2024-23-24',
        'Gröna Lund',
        'https://lol'
    )

    res = filter_keywords(venue, [event1, event2])
    assert res == [event2]

def test_filter_keywords_on_yml():
    venues = get_all_venues()
    grona_lund = venues[29]
    concerts = [
        Concert(
            'Halloween på Gröna Lund 2024', '2024-23-24', 'Gröna Lund', 'https://lol'
        ),
        Concert(
            'Tyrols Julbord är tillbaka!', '2024-23-24', 'Gröna Lund', 'https://lol'
        ),
    ]
    res = filter_keywords(grona_lund, concerts)
    assert not res

