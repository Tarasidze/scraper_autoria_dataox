import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="[%(level_name)s]: %(message)s",
    handlers=[
        logging.FileHandler("scraper.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
