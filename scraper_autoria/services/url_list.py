from __future__ import annotations
from typing_extensions import List

import multiprocessing
import datetime

from urllib.parse import urlencode, urljoin

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from scraper_autoria.services import scraper_config
from scraper_autoria.services.chrome_web_driver_init import get_web_driver
from scraper_autoria.services.loger import logging


class UrlList:
    def __init__(
            self,
            web_driver: webdriver = None,
    ) -> None:

        if not web_driver:
            self._web_driver = get_web_driver()
        else:
            self._web_driver = web_driver

    def create_url_pages_list(
            self,
            url: str,
    ) -> List[str]:

        page_quantity = self._get_number_of_pages(url)

        return [
            urljoin(
                url, '?' + urlencode(
                    {
                        "indexName": "auto",
                        "size": "20",
                        "page": str(page_number),
                    },

                )
            )
            for page_number in range(page_quantity)
        ]

    def _get_number_of_pages(self, url: str) -> int:
        """The function finds a number of pages and returns int."""

        url = urljoin(
            url,
            '?' + urlencode(
                    {
                        "indexName": "auto",
                        "size": "20",
                        "page": 0,
                    },

                )
            )

        self._web_driver.get(url)

        try:
            pagination = self._web_driver.find_element(
                By.XPATH, scraper_config.XPATH_PAGINATION
            )
        except NoSuchElementException:
            return 1

        return int(pagination.text.replace(" ", ""))

    def get_chunks(self, url: str):
        num = self._get_number_of_pages(url)
        # logging.info(
        #     f"Time: {datetime.datetime.now()},"
        #     f" found {num} pages"
        # )

        cpu_quantity = multiprocessing.cpu_count()
        current_range = range(0, num)
        chunk_size = int(len(current_range) / (cpu_quantity // 4))

        return [
            current_range[x:x+chunk_size]
            for x in range(0, len(current_range), chunk_size)
        ]

    @staticmethod
    def create_urls_list_from_range(url: str, local_range: range) -> List[str]:

        url = "https://auto.ria.com/uk/search/"

        return [
            urljoin(
                url, '?' + urlencode(
                    {
                        "indexName": "auto",
                        "size": "20",
                        "page": str(page_number),
                    },

                )
            )
            for page_number in local_range
        ]
