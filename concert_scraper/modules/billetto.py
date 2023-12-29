"""Fetch data from billetto.se"""

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

from concert_scraper.common import Concert

BASE_URL = "https://billetto.se"
By.CSS_SELECTOR


def get_concerts(venue, browser):
    browser.get(venue.url)
    time.sleep(5)
    concerts = set()

    try:
        cookie_button = browser.find_element(By.ID, "onetrust-accept-btn-handler")
        cookie_button.click()
    except NoSuchElementException:
        print("No cookie banner")

    time.sleep(1)

    while True:
        # Go through all pages
        html = browser.page_source

        def clean_date(date_str):
            dates = date_str.split("-")
            start_date = dates[0].strip()
            return start_date

        soup = BeautifulSoup(html, features="html.parser")

        # Sadly the elements can not be identified except for their combination of classes
        classes = "bg-white dark:bg-gray-800 flex flex-col justify-between relative border-gray-200 dark:border-gray-700 sm:rounded-lg divide-y divide-gray-200 dark:divide-gray-700 border shadow overflow-hidden"
        concert_elements = soup.find_all(name="div", attrs={'class': classes})
        for concert in concert_elements:
            title_attrs = {'class': 'block text-white hover:text-brand-500 font-medium text-base truncate'}
            concert_title = concert.find('a', attrs=title_attrs)
            if not concert_title or not len(concert_title.getText()):
                continue
            concert_title = concert_title.getText()

            date_attrs = {'class': 'border border-gray-200 p-1 text-xs text-brand-500 bg-white rounded-md'}
            concert_dates = clean_date(concert.find(attrs=date_attrs).get_text())

            concert_url = concert.find('a').get('href') if concert.find('a') else venue.url
            concerts.add(
                Concert(concert_title, concert_dates, venue.name, concert_url)
            )

        # Next page
        try:
            button = browser.find_element(By.CSS_SELECTOR, "[aria-label=Nästa]")
            if button.is_enabled():
                button.click()
            else:
                break
        except NoSuchElementException:
            break

    return concerts
