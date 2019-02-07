import logging
import time

from cmreslogging.handlers import CMRESHandler

from busbank.scraper import get_geoposes
from busbank.databaser import insert_raw_text


logger = logging.getLogger("BusBank")
logger.setLevel(logging.DEBUG)

elasticsearch_handler = CMRESHandler(hosts=[
    {
        "host": "localhost",
        "port": 9200,
    }],
    auth_type=CMRESHandler.AuthType.NO_AUTH,
    es_index_name="busbank",
)
elasticsearch_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(
    logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

logger.addHandler(console_handler)
logger.addHandler(elasticsearch_handler)


def fetch_data_then_store():
    logger.info("Executing fetch and store function")
    insert_raw_text(get_geoposes())


if __name__ == "__main__":
    logger.info("Starting BusBank")

    while True:
        fetch_data_then_store()
        time.sleep(10)
        