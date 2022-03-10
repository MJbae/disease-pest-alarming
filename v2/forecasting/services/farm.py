from typing import Set

from forecasting.dtos import ForecastingDto, AffectedFarmDto
from forecasting.models import Forecasting, User, Farm, Crop, ProducingCrop


def find_affected_farms(forecasting_set: Set[ForecastingDto]) -> Set[AffectedFarmDto]:
    """
    Find affected farms according to address and crop from forecasting data

    Parameters:
        forecasting_set(Set[ForecastingDto]): the latest forecasting data from open api

    Returns:
        affected_farm_set(Set[AffectedFarmDto]): contains affected farm's info
    """

    affected_farm_set = set()
    for owner in User.objects.filter(is_staff=False):
        for farm in Farm.objects.filter(owner=owner):
            for producing_crop in ProducingCrop.objects.filter(farm=farm):
                for forecasting in forecasting_set:
                    if _is_affected_farm(farm, forecasting, producing_crop):
                        affected_farm_set.add(AffectedFarmDto(contact=owner.phone_number, info=forecasting))

    return affected_farm_set


def _is_affected_farm(farm, forecasting, producing_crop):
    address_in_farm = farm.address.name
    address_in_forecasting = forecasting.address_name
    crop_in_producing_crop = producing_crop.crop.name
    crop_in_forecasting = forecasting.crop_name

    return crop_in_producing_crop == crop_in_forecasting and address_in_farm == address_in_forecasting
