from typing import Set

from domains import ForecastingDto, AffectedFarmDto


def collect_the_latest_forecasting() -> Set[ForecastingDto]:
    pass


def extract_influential_forecasting(forecasting: ForecastingDto) -> Set[ForecastingDto]:
    pass


def find_affected_farms(damages: Set[ForecastingDto]) -> Set[AffectedFarmDto]:
    pass


def send_alarms(farms: Set[AffectedFarmDto]):
    pass
