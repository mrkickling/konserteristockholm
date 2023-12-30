import requests
import os
import json
from concert_scraper.logger import get_logger

logger = get_logger()

def export_concerts(concerts):
    api_key = os.getenv('api_key')
    url = os.getenv('api_url')
    concerts = json.dumps(concerts)
    data = {"concerts": concerts, "api_key": api_key}

    logger.info(f"Sending {len(concerts)} concerts to {url}")

    requests.post(url, data=data)
