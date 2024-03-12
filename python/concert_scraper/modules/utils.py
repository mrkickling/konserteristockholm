def filter_keywords(venue, concerts):
    """Remove the concerts which contain any of the venues filtered keywords"""

    def any_keyword_in_string(string, keywords):
        for keyword in keywords:
            if keyword in string:
                return True
        return False

    return [
        concert for concert in concerts
        if not any_keyword_in_string(concert.title, venue.filter_keywords)
    ]
