import os
from datetime import datetime, date

import pytest
from model_bakery import baker

from forecasting.dtos import ForecastingDto, AffectedFarmDto
from forecasting.services.forecasting import collect_the_latest_forecasting
from forecasting.services.farm import find_affected_farms
from forecasting.services.alarm import send_alarms

pytestmark = [pytest.mark.django_db, pytest.mark.e2e]


def test_from_catching_the_latest_forecasting_to_sending_alarm():
    # mock forecasting
    owner = baker.make("forecasting.User", phone_number=os.environ.get("TEST_NUMBER"))
    address = baker.make('Address', code=123, name="가평군")
    crop = baker.make('Crop', code="F123", name="포도")
    farm = baker.make('Farm', owner=owner, address=address)
    baker.make('ProducingCrop', farm=farm, crop=crop)

    last_forecasting_date = datetime.strptime("2021-11-02", "%Y-%m-%d").date()
    baker.make('Forecasting', date=last_forecasting_date, _fill_optional=['address', 'crop', 'target'])

    # run main service logic
    forecasting_set = collect_the_latest_forecasting()
    farm_set = find_affected_farms(forecasting_set)
    result, success_to_send = send_alarms(farm_set)

    # check if the result is correct
    assert result == "success"
    assert success_to_send == 1
