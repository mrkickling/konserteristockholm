# https://www.facebook.com/restauranglandet/upcoming_hosted_events

"""Fetch data from scalateatern.se"""

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
from bs4 import BeautifulSoup
import time

from concert_scraper.common import Concert
from concert_scraper.logger import get_logger

logger = get_logger(__name__)

BASE_URL = "https://www.facebook.com/"

def parse_date(date_string):
    if date_string == "HAPPENING NOW":
        return datetime.now().strftime("%Y-%m-%d")

    # Format is FRI, 24 MAY AT 20:00
    weekday, month_str, date_str, *rest = date_string.split()
    date_str = date_str if len(date_str) == 2 else "0" + date_str
    month_str = month_str.capitalize()

    # Use 1904 first as it is a leap year
    date = datetime.strptime(f"1904 {date_str} {month_str}", '%Y %d %b')
    now = datetime.now()

    try:
        # Test previous year (might fail)
        date = date.replace(year=now.year)
    except ValueError:
        print("Failed to parse date - trying with next year instead")

    # Use next year if previous tested year was before now
    if date < now:
        date = date.replace(year=now.year+1)

    return date.strftime("%Y-%m-%d")
    
def get_concerts(venue, browser):
    logger.info(f"Getting concerts for venue {venue.name}")
    browser.get(venue.url)

    # Deny cookie and login popups
    time.sleep(2)

    try:
        cookie_button = browser.find_element(By.XPATH, "//*[contains(text(), 'Decline optional cookies')]")
        cookie_button.click()
    except NoSuchElementException:
        logger.info("Found no cookie popup - weird?")

    time.sleep(1)

    try:
        dont_login_button = browser.find_element(By.CSS_SELECTOR, '[aria-label="Close"]')
        dont_login_button.click()
    except NoSuchElementException:
        logger.info("Found no login popup - weird?")

    # Scroll to bottom
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Use xpaths to find all events
    concerts = []
    i = 1
    while True:
        # Thank you facebook for making me do this :/
        xpath = f"""
            /html/body/div[1]/div/div[1]/div/div[3]
            /div/div/div[1]/div[1]/div/div/div[4]
            /div/div/div/div/div/div/div/div/div[3]
            /div[{i}]/div[2]/div[1]/div
        """
 
        xpath_suffix_link = "/div[2]/span/span/div/a"
        xpath_suffix_title = "/div[2]/span/span/div/a/span"
        xpath_suffix_date = "/div[1]/span/span"

        # Try to find the elements using selenium
        try:
            title_element = browser.find_element(By.XPATH, xpath + xpath_suffix_title)
            date_element = browser.find_element(By.XPATH, xpath + xpath_suffix_date)
            link_element = browser.find_element(By.XPATH, xpath + xpath_suffix_link)
        except NoSuchElementException:
            # If we can not find by xpath we have to give up.
            break

        if not title_element or not date_element or not link_element:
            # If element is not found we should just give up
            break
        else:
            # Otherwise - nice, we fetch the values and create the Concert object
            title = title_element.text
            date = parse_date(date_element.text)
            url = link_element.get_attribute('href')
            
            # Make sure date was correctly parsed
            if date:
                concerts.append(
                    Concert(title, date, venue.name, url)
                )
            i += 1
    
    logger.info(f"Found {len(concerts)} concerts for venue {venue.name}")
    return concerts
