from dataclasses import dataclass
from datetime import date


@dataclass(unsafe_hash=True, frozen=True)
class ForecastingDto:
    date: date
    target_name: str
    crop_name: str
    address_name: str


@dataclass(unsafe_hash=True, frozen=True)
class AffectedFarmDto:
    contact: str
    info: ForecastingDto
