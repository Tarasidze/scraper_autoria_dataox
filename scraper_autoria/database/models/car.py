import datetime

from typing_extensions import Annotated

from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from scraper_autoria.database.data_base_init import Base


timestamp = Annotated[
    datetime.datetime,
    mapped_column(nullable=False, server_default=func.CURRENT_TIMESTAMP()),
]


class MyBase(Base):
    __abstract__ = True

    def to_dict(self):
        return {
            field.name: getattr(self, field.name) for field in self.__table__.c
        }


class Car(MyBase):

    __tablename__ = "car"

    url: Mapped[str] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    price_usd: Mapped[int] = mapped_column(nullable=False)
    odometer: Mapped[int] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[int] = mapped_column(nullable=False)
    image_url: Mapped[str] = mapped_column(nullable=False)
    images_count: Mapped[int]
    car_number: Mapped[str]
    car_vin: Mapped[str]
    datetime_found: Mapped[timestamp] = mapped_column(server_default=func.UTC_TIMESTAMP())
