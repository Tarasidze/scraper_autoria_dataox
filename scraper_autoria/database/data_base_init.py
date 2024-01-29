"""The module configure database"""
import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


load_dotenv()

pg_db_name = os.getenv("POSTGRES_DB")
pg_user = os.getenv("POSTGRES_USER")
pg_pass = os.getenv("POSTGRES_PASSWORD")
pg_host = os.getenv("POSTGRES_HOST")
pg_port = os.getenv("POSTGRES_PORT")

URL_DATABASE = f"postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db_name}"

engine = create_engine(URL_DATABASE)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
session_local = SessionLocal()
