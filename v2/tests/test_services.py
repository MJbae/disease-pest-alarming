from datetime import datetime, date

import pytest
from model_bakery import baker

from ..forecasting.domains import ForecastingDto
from ..forecasting.services import collect_the_latest_forecasting, find_affected_farms

pytestmark = [pytest.mark.django_db]


def test_collect_the_latest_forecasting():
    # 1. mock forecasting
    latest_date = datetime.strptime("2021-11-02", "%Y-%m-%d").date()
    earliest_date = datetime.strptime("2021-10-26", "%Y-%m-%d").date()

    baker.make('Forecasting', date=earliest_date, _fill_optional=['address', 'crop', 'target'])
    forecasting_from_db = baker.make('Forecasting', date=latest_date, _fill_optional=['address', 'crop', 'target'])

    # 2. 최신 예찰정보를 Set[ForecastingDto] 형태로 반환
    forecasting_set = collect_the_latest_forecasting()

    # 3. forecasting_set 내 모든 구성요소의 date가 최신 날짜를 가리키는지 체크
    for forecasting in forecasting_set:
        assert forecasting.date > forecasting_from_db.date


def test_find_affected_farms():
    # mock forecasting dto set
    forecasting_set = set()
    forecasting_dto_1st = ForecastingDto(date=date.today(), target_name="test_pest", crop_name="포도", address_name="가평군")
    forecasting_dto_2nd = ForecastingDto(date=date.today(), target_name="test_pest", crop_name="포도", address_name="화성시")
    forecasting_set.add(forecasting_dto_1st)
    forecasting_set.add(forecasting_dto_2nd)

    # mock Farm and Owner

    # return affected farms
    farm_set = find_affected_farms(forecasting_set)

    # test returned farms are valid


def test_send_alarms():
    pass
