import requests
import os
import json
from concert_scraper.logger import get_logger

logger = get_logger(__name__)

def export_concerts(concerts):
    for i in range(0, len(concerts), 100):
        part_concerts = concerts[i:i + 100]
        api_key = os.getenv('api_key')
        url = os.getenv('api_url')
        part_concerts = json.dumps([concert.__dict__ for concert in part_concerts])
        data = {"concerts": part_concerts, "api_key": api_key}

        logger.info(f"Sending concerts to {url}")
        res = requests.post(url, data=data)
        logger.info(res.text)