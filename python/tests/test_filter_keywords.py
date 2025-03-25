from concert_scraper.common import Concert, Venue
from concert_scraper.modules.utils import (
    concerts_with_include_keywords,
    concerts_without_exclude_keywords
)
from concert_scraper.scraper import get_all_venues

def test_exclude_keywords():
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

    res = concerts_without_exclude_keywords(venue, [event1, event2])
    assert res == [event2]

def test_exclude_keywords_on_yml():
    venues = get_all_venues()
    venue = next(v for v in venues if v.name == 'Gröna Lund')
    concerts = [
        Concert(
            'Halloween på Gröna Lund 2024', '2024-23-24', 'Gröna Lund', 'https://lol'
        ),
        Concert(
            'Tyrols Julbord är tillbaka!', '2024-23-24', 'Gröna Lund', 'https://lol'
        ),
    ]
    res = concerts_without_exclude_keywords(venue, concerts)
    assert not res


def test_include_keywords():
    venue = Venue(
        "Gröna Lund",
        "Stockholm",
        "?",
        "https://",
        [],
        ['Jazz']
    )
    event1 = Concert(
        'Jazz',
        '2024-23-24',
        'Gröna Lund',
        'https://lol'
    )
    event2 = Concert(
        'Biografvisning',
        '2024-23-24',
        'Gröna Lund',
        'https://lol'
    )

    res = concerts_with_include_keywords(venue, [event1, event2])
    assert res == [event1]

def test_include_keywords_on_yml():
    venues = get_all_venues()
    venue = next(v for v in venues if v.name == "Biocafé Tellus")
    concerts = [
        Concert(
            'Halloween på Gröna Lund 2024',
            '2024-23-24',
            'Gröna Lund',
            'https://lol'
        ),
        Concert(
            'Tyrols Julbord är tillbaka!',
            '2024-23-24',
            'Gröna Lund',
            'https://lol'
        ),
        Concert(
            'Jazz!',
            '2024-23-24',
            'Gröna Lund',
            'https://lol'
        ),
    ]
    res = concerts_with_include_keywords(venue, concerts)
    assert len(res) == 1
    assert res[0].title == "Jazz!"
