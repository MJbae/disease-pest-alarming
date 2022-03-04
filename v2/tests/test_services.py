from datetime import datetime

import pytest
from model_bakery import baker

pytestmark = [pytest.mark.django_db]

from forecasting.services import collect_the_latest_forecasting


def test_collect_the_latest_forecasting():
    # 1. forecasting mocking
    latest_date = datetime.strptime("2021-11-02", "%Y-%m-%d").date()
    earliest_date = datetime.strptime("2021-10-26", "%Y-%m-%d").date()

    baker.make('Forecasting', date=earliest_date, _fill_optional=['address', 'crop', 'target'])
    latest_forecasting = baker.make('Forecasting', date=latest_date, _fill_optional=['address', 'crop', 'target'])

    # 2. 최신 예찰정보를 다음의 형태로 반환, Set[ForecastingDto]
    forecasting_set = collect_the_latest_forecasting()

    # 3. forecasting_set 내 모든 구성요소의 date가 최신 날짜를 가리키는지 체크
    for forecasting in forecasting_set:
        assert forecasting.date > latest_forecasting.date


def test_extract_influential_forecasting():
    pass


def test_find_affected_farms():
    pass


def test_send_alarms():
    pass
