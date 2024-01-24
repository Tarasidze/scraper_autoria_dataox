"""Module provides save data to database and damp database to file."""

from __future__ import annotations
import os
import datetime
import subprocess

from scraper_autoria.database.data_base_init import SessionLocal
from scraper_autoria.database.models.car import Car
from scraper_autoria.services.loger import logging

from dotenv import load_dotenv


load_dotenv()


class CarDbManager:
    @staticmethod
    def save_car_to_database(cat_data_: Car, session_: SessionLocal) -> None:
        """Save car to database."""
        session_.add(cat_data_)
        session_.commit()

    @staticmethod
    def dump_database_to_file() -> None:
        """Backup postgres db to a file."""
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
        filename = f"database_{current_datetime}.sql"
        file_path = os.path.abspath(os.path.join("dumps", filename))

        os.makedirs("dumps", exist_ok=True)

        try:
            process = subprocess.Popen(
                [
                    "pg_dump",
                    "--dbname=postgresql://{}:{}@{}:{}/{}".format(
                         os.getenv("POSTGRES_USER"),
                         os.getenv("POSTGRES_PASSWORD"),
                         os.getenv("POSTGRES_HOST"),
                         os.getenv("PORT"),
                         os.getenv("POSTGRES_DB"),
                    ),
                    "-f", file_path
                ],
                stdout=subprocess.PIPE
            )

            if process.returncode != 0:
                logging.info(f"Time: {datetime.datetime.now()},"
                             f" database dumped"
                             f"{process.communicate()[0]}"
                             )
                exit(1)

        except Exception as e:
            logging.info(f"Time: {datetime.datetime.now()},"
                         f" Dump database error{e}.")
            exit(1)
