import time

from busbank.scraper import get_geoposes
from busbank.databaser import insert_raw_text


def fetch_data_then_store():
    print("Getting geopos")
    insert_raw_text(get_geoposes())


if __name__ == "__main__":
    print("hi")

    while True:
        fetch_data_then_store()
        time.sleep(10)
        