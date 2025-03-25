from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..common import Venue, Concert

months_se = [
    "januari",
    "februari",
    "mars",
    "april",
    "maj",
    "juni",
    "juli",
    "augusti",
    "september",
    "oktober",
    "november",
    "december"
]

short_months_se = [
    "jan",
    "feb",
    "mar",
    "apr",
    "maj",
    "jun",
    "jul",
    "aug",
    "sep",
    "okt",
    "nov",
    "dec"
]

short_months_en = [
    "jan",
    "feb",
    "mar",
    "apr",
    "may",
    "jun",
    "jul",
    "aug",
    "sep",
    "oct",
    "nov",
    "dec"
]

def _has_one_of_keywords_in_string(string: str, keywords: list[str]):
    return any(
        keyword for keyword in keywords if keyword.lower() in string.lower()
    )

def concerts_without_exclude_keywords(
        venue: Venue, concerts: list[Concert]
    ):
    """
    Return the concerts which do not contain any of the venues
    exclude keywords.
    """

    if not venue.exclude_keywords:
        return concerts

    return [
        concert for concert in concerts
        if not _has_one_of_keywords_in_string(
            concert.title, venue.exclude_keywords
        )
    ]

def concerts_with_include_keywords(venue: Venue, concerts: list[Concert]):
    """
    Return the concerts which contain any of the venues include keywords.
    """

    if not venue.include_keywords:
        return concerts

    return [
        concert for concert in concerts
        if _has_one_of_keywords_in_string(
            concert.title, venue.include_keywords
        )
    ]
