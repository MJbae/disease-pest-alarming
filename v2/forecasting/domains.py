from dataclasses import dataclass
from datetime import date


class Crop:
    code: str
    name: str


class Address:
    code: str
    name: str


@dataclass(unsafe_hash=True)
class ForecastingDto:
    target: str
    date: date
    crop: str
    address: str


@dataclass(unsafe_hash=True)
class AffectedFarmDto:
    contact: str
    info: ForecastingDto
