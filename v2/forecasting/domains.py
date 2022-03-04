from dataclasses import dataclass
from datetime import date


class Crop:
    code: str
    name: str


class Address:
    code: str
    name: str


class Target:
    name: str


@dataclass(unsafe_hash=True)
class ForecastingDto:
    date: date
    target: str
    crop: str
    address: str


@dataclass(unsafe_hash=True)
class AffectedFarmDto:
    contact: str
    info: ForecastingDto


class Forecasting:
    def __init__(self, date: date, address: Address, crop: Crop, target: Target):
        self.date = date
        self.address = address
        self.crop = crop
        self.target = target
