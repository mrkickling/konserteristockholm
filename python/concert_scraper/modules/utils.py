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

def filter_keywords(venue, concerts):
    """
    Remove the concerts which contain any of the venues filtered keywords
    """

    def any_keyword_in_string(string, keywords):
        for keyword in keywords:
            if keyword in string:
                return True
        return False

    return [
        concert for concert in concerts
        if not any_keyword_in_string(concert.title, venue.filter_keywords)
    ]
