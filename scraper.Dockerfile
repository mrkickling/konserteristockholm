FROM python-3.11-alpine

COPY src/concert_scraper /opt/concert_scraper
ENTRYPOINT [ "scraper_entrypoint.sh" ]