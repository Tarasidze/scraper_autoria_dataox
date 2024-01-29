import datetime
import multiprocessing
from multiprocessing import Process
from threading import Thread

import schedule

from scraper_autoria.services.scraper import Scraper
from scraper_autoria.database.database_manager import CarDbManager

from scraper_autoria.services.loger import logging
from scraper_autoria.services.url_list import UrlList


BASE_URL = "https://auto.ria.com/uk/car/used/"


def run_multithreading():
    """Multithreading function"""
    thread_workers = []

    chunks = UrlList().get_chunks(BASE_URL)

    for chunk in chunks:
        t = Thread(target=Scraper(BASE_URL).scrap_all_pages, args=([chunk]))
        thread_workers.append(t)
        t.start()

    for t in thread_workers:
        t.join()


def run_multiprocessing():
    processes = []

    chunks = UrlList().get_chunks(BASE_URL)

    for chunk in chunks:
        p = Process(target=Scraper(BASE_URL).scrap_all_pages, args=([chunk]))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()


if __name__ == '__main__':

    db_manager = CarDbManager()

    logging.info(
        f"Time: {datetime.datetime.now()}, "
        f"instances of database manager created."
    )

    schedule.every().day.at("05:29").do(run_multithreading())
    schedule.every().day.at("00:00").do(db_manager.dump_database_to_file)

    while True:
        schedule.run_pending()






