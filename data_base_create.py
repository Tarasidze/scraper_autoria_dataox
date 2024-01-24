import datetime
from time import sleep
from scraper_autoria.services.loger import logging
from scraper_autoria.database.models.car import Car
from scraper_autoria.database.data_base_init import (
    Base,
    engine
)


def create_db():
    Base.metadata.create_all(engine)
    logging.info(f"Time: {datetime.datetime.now()}, Database created.")
    sleep(2)


if __name__ == "__main__":
    create_db()
