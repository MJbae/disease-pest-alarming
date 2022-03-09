import os
from datetime import datetime, date

import pytest
from model_bakery import baker

from forecasting.domains import ForecastingDto, AffectedFarmDto
from forecasting.services.forecasting import collect_the_latest_forecasting
from forecasting.services.farm import find_affected_farms
from forecasting.services.alarm import send_alarms

pytestmark = [pytest.mark.django_db]


def test_can_collect_later_dated_forecasting():
    # mock forecasting
    latest_date = datetime.strptime("2021-11-02", "%Y-%m-%d").date()
    earliest_date = datetime.strptime("2021-10-26", "%Y-%m-%d").date()

    baker.make('Forecasting', date=earliest_date, _fill_optional=['address', 'crop', 'target'])
    forecasting_from_db = baker.make('Forecasting', date=latest_date, _fill_optional=['address', 'crop', 'target'])

    # 최신 예찰정보를 Set[ForecastingDto] 형태로 반환
    forecasting_set = collect_the_latest_forecasting()

    # forecasting_set 내 모든 구성요소의 date가 최신 날짜를 가리키는지 체크
    for forecasting in forecasting_set:
        assert forecasting.date > forecasting_from_db.date


def test_can_find_affected_farms():
    # mock persistent data
    owner = baker.make("forecasting.User", phone_number="01012341234")
    address = baker.make('Address', code=123, name="가평군")
    crop = baker.make('Crop', code="F123", name="포도")
    farm = baker.make('Farm', owner=owner, address=address)
    baker.make('ProducingCrop', farm=farm, crop=crop)

    # mock forecasting dto set
    forecasting_set = set()
    forecasting_dto = ForecastingDto(date=date.today(),
                                     target_name="test_pest",
                                     crop_name="포도",
                                     address_name="가평군")
    forecasting_set.add(forecasting_dto)

    # return affected farms
    farm_set = find_affected_farms(forecasting_set)
    farm = farm_set.pop()

    # test returned farms are valid
    assert farm.contact == owner.phone_number
    assert farm.info == forecasting_dto


def test_can_filter_not_affected_farms():
    # mock persistent data
    owner = baker.make("forecasting.User", phone_number="01012341234")
    address = baker.make('Address', code=123, name="테스트시")
    crop = baker.make('Crop', code="F123", name="테스트작물")
    farm = baker.make('Farm', owner=owner, address=address)
    baker.make('ProducingCrop', farm=farm, crop=crop)

    # mock forecasting dto set
    forecasting_set = set()
    forecasting_dto = ForecastingDto(date=date.today(),
                                     target_name="test_pest",
                                     crop_name="test_crop",
                                     address_name="test_address")
    forecasting_set.add(forecasting_dto)

    # return affected farms
    farm_set = find_affected_farms(forecasting_set)

    # test returned farms are valid
    with pytest.raises(KeyError, match='pop from an empty set'):
        farm_set.pop()


def test_can_send_alarms_to_all_affected_farm_owners():
    # mock Set[AffectedFarmDto]
    affected_farm_set = set()
    forecasting_dto = ForecastingDto(date=date.today(),
                                     target_name="test_pest",
                                     crop_name="포도",
                                     address_name="가평군")
    affected_farm = AffectedFarmDto(contact=os.environ.get("TEST_NUMBER"), info=forecasting_dto)
    affected_farm_set.add(affected_farm)

    # return result of sending alarms
    result, success_to_send = send_alarms(affected_farm_set)

    # check if the result is correct
    assert result == "success"
    assert success_to_send == 1
