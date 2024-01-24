"""Main module for parsing https://auto.ria.com/uk/car/used/"""
from __future__ import annotations

import datetime
from urllib.parse import urlencode, urljoin
from time import sleep


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common import (
    NoSuchElementException,
)

from scraper_autoria.database.database_manager import CarDbManager
from scraper_autoria.services import scraper_config
from scraper_autoria.database.data_base_init import SessionLocal
from scraper_autoria.database.models.car import Car
from scraper_autoria.services.loger import logging


class Scraper:
    """Class provides collecting necessary information from autoria.com."""
    def __init__(
            self,
            web_driver: webdriver,
            base_url: str,
            session: SessionLocal
    ) -> None:
        self._web_driver = web_driver
        self._base_url = base_url
        self._session = session

    @staticmethod
    def _click_on_cookies(driver_: webdriver):
        """The function wait on cookies frame and click on it"""
        wait = WebDriverWait(driver_, 10)

        cookies_button_locator = (
            By.CSS_SELECTOR, scraper_config.CSS_SELECTOR_COOKIES_BUTTON
        )
        cookies_button = wait.until(
            expected_conditions.element_to_be_clickable(cookies_button_locator)
        )
        sleep(0.2)
        cookies_button.click()

    def _get_number_of_pages(self) -> int:
        """The function finds a number of pages and returns int."""

        try:
            pagination = self._web_driver.find_element(
                By.XPATH, scraper_config.XPATH_PAGINATION
            )
        except NoSuchElementException:
            return 1

        return pagination.text.replace(" ", "")

    @staticmethod
    def _get_all_car_links_from_page(driver_: webdriver) -> list:
        """Function collects all references from specific page."""
        links = driver_.find_elements(
            By.CLASS_NAME, scraper_config.CLASS_CAR_LINKS
        )

        return [
            link.get_attribute("href") for link in links
        ]

    @staticmethod
    def _get_phone_number(driver_: webdriver) -> int:
        """The function gets phon number"""

        phone_button = driver_.find_element(By.XPATH, scraper_config.XPATH_CAR_PHONE_BTN)
        driver_.execute_script("arguments[0].click();", phone_button)

        sleep(0.05)

        phone_number = driver_.find_element(
            By.XPATH, scraper_config.XPATH_CAR_PHONE_2
        )

        driver_.execute_script("arguments[0].click();", phone_number)

        sleep(0.05)

        phone_number = "38" + phone_number.text

        return int(phone_number.replace(" ", "").replace("(", "").replace(")", ""))

    @staticmethod
    def _get_vin_code(driver_: webdriver) -> str | None:
        """The function gets car's vin code"""
        driver_.refresh()
        try:
            vin = driver_.find_element(By.CLASS_NAME, scraper_config.CLASS_VIN_1)
        except NoSuchElementException:
            try:
                vin = driver_.find_element(By.XPATH, scraper_config.XPATH_CAR_VIN)
            except NoSuchElementException:
                return None

        return vin.text

    @staticmethod
    def _get_car_number(driver_: webdriver) -> str | None:
        """The function gets car number"""
        try:
            car_number = driver_.find_element(
                By.CSS_SELECTOR, scraper_config.CSS_SELECTOR_CAR_NUMBER
            ).text
        except NoSuchElementException:
            return None

        return car_number

    @staticmethod
    def _get_car_image_url(driver_: webdriver, car_url: str) -> str | None:
        """The function get image url"""
        try:
            img_url = driver_.find_element(
                    By.XPATH, scraper_config.XPATH_CAR_IMAGE_URL
                ).get_attribute("srcset")
        except NoSuchElementException:
            try:
                img_url = driver_.find_element(
                    By.XPATH, scraper_config.XPATH_CAR_IMAGE_URL_2
                ).get_attribute("srcset")
            except NoSuchElementException:
                return "None"
        return img_url

    def get_car_data(self, link: str, driver_: webdriver) -> Car | None:
        """Collect all information from car page"""
        driver_.get(link)

        try:
            driver_.find_element(By.CLASS_NAME, scraper_config.CLASS_NOTICE_HEAD)
        except NoSuchElementException:
            return Car(
                url=link,
                title=driver_.find_element(
                    By.CSS_SELECTOR, scraper_config.CSS_SELECTOR_TITLE
                ).text,
                price_usd=int(driver_.find_element(
                    By.CLASS_NAME, scraper_config.CLASS_CAR_PRICE
                ).text.split("$")[0].replace(" ", "")),
                odometer=int(driver_.find_element(
                    By.XPATH, scraper_config.XPATH_CAR_ODOMETER
                ).text.split()[0]) * 1000,
                username=driver_.find_element(
                    By.CSS_SELECTOR, scraper_config.CSS_SELECTOR_USERNAME
                ).get_attribute("title"),
                image_url=self._get_car_image_url(driver_=driver_, car_url=link),
                images_count=int(
                    driver_.find_element(
                        By.XPATH, scraper_config.XPATH_CAR_IMG_COUNT
                    ).text.split()[-1]
                ),
                car_number=self._get_car_number(driver_=driver_),
                car_vin=self._get_vin_code(driver_=driver_),
                datetime_found=None,
                phone_number=self._get_phone_number(driver_=driver_),
            )

        return None

    def scrap_all_pages(self):
        """Main unction in scraper class"""
        driver = self._web_driver
        driver.get(self._base_url)

        self._click_on_cookies(driver_=driver)
        number_of_pages = self._get_number_of_pages()

        page_parameters = {"page": 0}

        for page_number in range(2):
            logging.info(f"Time: {datetime.datetime.now()}, scrapping started.")

            page_parameters["page"] = page_number
            url = urljoin(self._base_url, '?' + urlencode(page_parameters))
            driver.get(url)

            car_db_manager = CarDbManager()

            urls_list = self._get_all_car_links_from_page(driver_=driver)

            if not urls_list:
                break

            for car_url in urls_list:
                car_data = self.get_car_data(link=car_url, driver_=driver)

                if not car_data:
                    break

                car_db_manager.save_car_to_database(
                    cat_data_=car_data,
                    session_=self._session
                )

        logging.info(f"Time: {datetime.datetime.now()}, scraper ends his job.")

