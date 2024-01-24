import datetime
import schedule
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from scraper_autoria.services.scraper import Scraper
from scraper_autoria.database.data_base_init import session
from scraper_autoria.database.database_manager import CarDbManager

from scraper_autoria.services.loger import logging


CHROME_OPTIONS = "--headless=new"
BASE_URL = "https://auto.ria.com/uk/car/used/"

options = Options()
prefs = {"profile.default_content_setting_values.notifications": 2}
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=options)


if __name__ == '__main__':

    scraper = Scraper(web_driver=driver, base_url=BASE_URL, session=session)
    db_manager = CarDbManager()

    logging.info(
        f"Time: {datetime.datetime.now()}, "
        f"instances of scraper and database manager created."
    )

    schedule.every().day.at("12:00").do(scraper.scrap_all_pages)
    schedule.every().day.at("00:00").do(db_manager.dump_database_to_file)

    while True:
        schedule.run_pending()
