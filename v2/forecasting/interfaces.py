import abc
from domains import ForecastingDto, DamageDto, DamagedFarmDto
from typing import Set


class ICollector(abc.ABC):
    @abc.abstractmethod
    def collect_the_latest_forecasting(self) -> ForecastingDto:
        raise NotImplementedError


class IDamageExtractor(abc.ABC):
    @abc.abstractmethod
    def extract_damages(self, forecasting: ForecastingDto) -> Set[DamageDto]:
        raise NotImplementedError


class IFarm(abc.ABC):
    @abc.abstractmethod
    def find_damaged_farms(self, damages: Set[DamageDto]) -> Set[DamagedFarmDto]:
        raise NotImplementedError


class IAlarm(abc.ABC):
    @abc.abstractmethod
    def send_alarm(self, farms: Set[DamagedFarmDto]):
        raise NotImplementedError

