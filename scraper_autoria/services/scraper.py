"""Main module for parsing https://auto.ria.com/uk/car/used/"""
from __future__ import annotations

import datetime
from time import sleep
import re

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common import (
    NoSuchElementException,
)

from scraper_autoria.database.database_manager import CarDbManager
from scraper_autoria.services import scraper_config
from scraper_autoria.database.models.car import Car
from scraper_autoria.services.loger import logging
from scraper_autoria.services.chrome_web_driver_init import get_web_driver
from scraper_autoria.services.url_list import UrlList


BASE_URL = "https://auto.ria.com/uk/car/used/"


class Scraper:
    """Class provides collecting necessary information from autoria.com."""
    def __init__(
            self,
            base_url: str,
            web_driver: webdriver = None,
    ) -> None:
        self._base_url = base_url

        if not web_driver:
            self._web_driver = get_web_driver()
        else:
            self._web_driver = web_driver

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
    def _get_car_image_url(driver_: webdriver) -> str | None:
        """The function get image url"""
        try:
            img_url = driver_.find_element(
                    By.XPATH, scraper_config.XPATH_CAR_IMAGE_URL
                ).get_attribute("srcset")
        except NoSuchElementException:
            try:
                img_url = driver_.find_element(
                    By.CLASS_NAME, scraper_config.CLASS_VIDEO
                ).get_attribute("srcset")
            except NoSuchElementException:
                return "None"
        return img_url

    @staticmethod
    def _get_car_title(driver_: webdriver) -> str | None:
        """Receive car title"""
        try:
            title = driver_.find_elements(
                    By.CSS_SELECTOR, scraper_config.CSS_SELECTOR_TITLE
                )
        except NoSuchElementException as e:
            # logging.info(f"Time: {datetime.datetime.now()}, Error No Title: {e}. , {driver_.current_url}")
            return "невідомо"

        return title[-1].text

    @staticmethod
    def _get_car_price(driver_: webdriver) -> int | None:
        """""Receive car price"""
        try:
            price_obj = driver_.find_element(
                    By.CLASS_NAME, scraper_config.CLASS_CAR_PRICE
                )
            price = int(re.sub(r"\D", "", price_obj.text))
        except (NoSuchElementException, Exception) as e:
            # logging.info(
            #     f"Time: {datetime.datetime.now()},"
            #     f" Error No Price: {e}. , {driver_.current_url}"
            # )
            return 0

        return price

    @staticmethod
    def _get_username(driver_: webdriver) -> str:
        """Receive username"""
        try:
            username = driver_.find_element(
                By.CSS_SELECTOR, scraper_config.CSS_SELECTOR_USERNAME
            ).get_attribute("title")
        except NoSuchElementException:
            try:
                username = driver_.find_element(
                    By.CSS_SELECTOR, scraper_config.CSS_SELECTOR_USERNAME_2
                ).text
            except NoSuchElementException:
                # logging.info(
                #     f"Time: {datetime.datetime.now()},"
                #     f" Error No Name {e}. , {driver_.current_url}"
                # )
                return "невідомо"

        return username

    @staticmethod
    def get_car_odometer(driver_: webdriver) -> int:
        """Receive odometer number"""
        try:
            odometer = driver_.find_element(
                By.XPATH, scraper_config.XPATH_CAR_ODOMETER
            ).text
            odometer = int(re.sub(r"\D", "", odometer))
        except (NoSuchElementException, Exception) as e:
            # logging.info(
            #     f"Time: {datetime.datetime.now()},"
            #     f" Error No oddometer {e}. , {driver_.current_url}"
            # )
            return 0

        return odometer * 1000

    @staticmethod
    def get_img_count(driver_: webdriver) -> int:
        """Receive quantity of pages """
        try:
            images_count = driver_.find_element(
                    By.XPATH, scraper_config.XPATH_CAR_IMG_COUNT
                ).text.split()[-1]
        except (NoSuchElementException, Exception) as e:
            # logging.info(
            #     f"Time: {datetime.datetime.now()},"
            #     f" Error No images {e}. , {driver_.current_url}"
            # )
            return 0

        return int(images_count)

    def get_car_data(self, link: str, driver_: webdriver) -> Car | None:
        """Collect all information from car page"""
        driver_.get(link)

        try:
            driver_.find_element(By.CLASS_NAME, scraper_config.CLASS_NOTICE_HEAD)
        except NoSuchElementException:
            return Car(
                url=link,
                title=self._get_car_title(driver_=driver_),
                price_usd=self._get_car_price(driver_=driver_),
                odometer=self.get_car_odometer(driver_=driver_),
                username=self._get_username(driver_=driver_),
                image_url=self._get_car_image_url(driver_=driver_),
                images_count=self.get_img_count(driver_=driver_),
                car_number=self._get_car_number(driver_=driver_),
                car_vin=self._get_vin_code(driver_=driver_),
                datetime_found=None,
                phone_number=self._get_phone_number(driver_=driver_),
            )

        return None

    def scrap_all_pages(self, url_range: range) -> None:
        """Function scraps received pages."""
        try:
            car_db_manager = CarDbManager()

            logging.info(f"Time: {datetime.datetime.now()}, scraper starts his job.")

            driver = get_web_driver()
            link_list = UrlList.create_urls_list_from_range(BASE_URL, url_range)

            driver.get(link_list[0])
            self._click_on_cookies(driver_=driver)

            for link in link_list:

                driver.get(link)
                car_urls_list = self._get_all_car_links_from_page(driver_=driver)

                if not car_urls_list:
                    return

                for car_url in car_urls_list:
                    car_data = self.get_car_data(link=car_url, driver_=driver)

                    if not car_data:
                        break

                    car_db_manager.save_car_to_database(cat_data_=car_data)

        except Exception as e:
            logging.info(f"Time: {datetime.datetime.now()}, Error {e}. , {link}")
            driver.close()
            self._web_driver.close()
            exit()

        driver.close()
        self._web_driver.close()
        logging.info(f"Time: {datetime.datetime.now()}, scraper ends his job.")
        exit()
