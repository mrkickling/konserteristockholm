from dataclasses import dataclass, field
from datetime import datetime, timedelta

@dataclass
class Concert:
    title: str
    date: str
    venue: str
    url: str

    def __hash__(self) -> int:
        return hash(self.url)

    def __str__(self):
        return f"{self.venue}: {self.title} - {self.date}"


@dataclass
class Venue:
    name: str
    location: str
    type: str
    url: str
    exclude_keywords: list = field(default_factory=list)
    include_keywords: list = field(default_factory=list)


def get_current_date():
    return datetime.now()


def get_probable_leap_year():
    """Either give current year, one year back or next leap year"""
    now = get_current_date()
    leap_year_diff = now.year % 4

    if leap_year_diff == 0:
        return now.year
    elif leap_year_diff == 1:
        return now.year - 1
    else:
        return now.year + (4 - leap_year_diff)


def get_future_date(month_int, day_int):
    """Take a month and day and try to find out what year it should be in"""

    # First create a date assuming leap year
    now = get_current_date()
    year = now.year

    # If leap day, set to probable year
    leap_day = month_int == 2 and day_int == 29
    if leap_day:
        year = get_probable_leap_year()

    # If date has already happened, add year
    date = datetime(year, month_int, day_int)
    if date < now - timedelta(1) and not leap_day:
        date = date.replace(year=now.year + 1)

    return date
