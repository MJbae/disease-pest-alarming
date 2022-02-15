from forecasting.models import Crop
from forecasting.serializers import FarmSerializer, ProducingCropSerializer


def save_nested_models_in_new_user(farms, user_id):
    """
    Save Farm and ProducingCrop Model instances according to User Model's id

    Parameters:
        farms(list): list with Farm model instance elements

    Returns:
        None
    """
    for farm in farms:
        crops = _get_crops(farm, user_id)
        farm_instance = _save_farm_instance(farm)

        for crop in crops:
            crop = _reformat_crop(crop, farm_instance.pk)
            _save_crop_instance(crop)


def _save_crop_instance(crop):
    serialized_crop = ProducingCropSerializer(data=crop)
    serialized_crop.is_valid()
    serialized_crop.save()


def _reformat_crop(crop, farm_pk):
    crop_name = crop.get("name")
    crop["farm"] = farm_pk
    crop_code = Crop.objects.get(name=crop_name).code
    crop["crop"] = crop_code
    del (crop['name'])

    return crop


def _save_farm_instance(farm):
    serialized_farm = FarmSerializer(data=farm)
    serialized_farm.is_valid()
    farm_instance = serialized_farm.save()
    return farm_instance


def _get_crops(farm, user_id):
    farm["owner"] = user_id
    crops = farm.get("producing_crops")
    return crops
