import abc
from domains import ForecastingDto, AffectedFarmDto
from typing import Set


class ICollector(abc.ABC):
    @abc.abstractmethod
    def collect_the_latest_forecasting(self) -> Set[ForecastingDto]:
        raise NotImplementedError


class IDamageExtractor(abc.ABC):
    @abc.abstractmethod
    def extract_influential_forecasting(self, forecasting: ForecastingDto) -> Set[ForecastingDto]:
        raise NotImplementedError


class IFarm(abc.ABC):
    @abc.abstractmethod
    def find_affected_farms(self, damages: Set[ForecastingDto]) -> Set[AffectedFarmDto]:
        raise NotImplementedError


class IAlarm(abc.ABC):
    @abc.abstractmethod
    def send_alarm(self, farms: Set[AffectedFarmDto]):
        raise NotImplementedError

