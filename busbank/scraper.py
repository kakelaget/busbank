import logging
import requests

from time import process_time

API_URL = "https://api.entur.org/anshar/1.0/rest/vm"

logger = logging.getLogger("BusBank")

def get_geoposes() -> str:
    start_time = process_time()
    logger.debug("Scraping API", extra={
        "API_URL": API_URL,
        "start_time": start_time,
    })

    response = requests.get(API_URL, headers={
        "ET-ClientName": "busbank-miljohackknowit",
    })

    end_time = process_time()
    total_time = end_time - start_time

    logger.info(f"Scraped API in {total_time:.3f}s", extra={
        "API_URL": API_URL,
        "start_time": start_time,
        "end_time": end_time,
        "total_time": total_time
    })

    if response.status_code != 200:
        logger.error(f"API returned HTTP {response.status_code}, expected HTTP 200", extra={
            "API_URL": API_URL,
            "status_code": response.status_code,
            "start_time": start_time,
            "end_time": end_time,
            "total_time": total_time
        })
        return ""
    
    return response.text
