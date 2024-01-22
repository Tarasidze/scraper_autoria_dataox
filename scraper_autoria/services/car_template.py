import dataclasses
from datetime import datetime


@dataclasses.dataclass
class CarTemplate:
    url: str
    title: str
    price_usd: int
    odometer: int
    username: str
    phone_number: int
    img_url: str
    images_count: int
    car_number: str
    car_vin: str
    datetime_found: None
