from os import getenv
from dotenv import load_dotenv
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from scraper_autoria.services.loger import logging


load_dotenv()

pg_db_name = getenv("POSTGRES_DB")
pg_user = getenv("POSTGRES_USER")
pg_pass = getenv("POSTGRES_PASSWORD")
pg_host = getenv("POSTGRES_HOST")
pg_port = getenv("POSTGRES_PORT")


URL_DATABASE = URL.create(
    "postgresql+pg8000",
    username=pg_user,
    password=pg_pass,
    host=pg_host,
    database=pg_port,
)

engine = create_engine(URL_DATABASE)
SessionLocal = sessionmaker(autoflush=False, bind=engine)
Base = declarative_base()

logging.info(f"Time: {datetime.now()}, Database created. Name: {pg_user}")
