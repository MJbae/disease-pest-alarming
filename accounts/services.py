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
        farm["owner"] = user_id
        farm_instance = _save_farm_instance(farm)
        crops = farm.get("producing_crops")

        for crop in crops:
            crop_code = crop.get("code")
            if crop_code:
                _save_producing_crop_instance(crop_code, farm_instance.pk)


def _save_producing_crop_instance(crop_code, farm_id):
    serialized_crop = ProducingCropSerializer(data={
        "farm": farm_id,
        "crop": crop_code
    })
    serialized_crop.is_valid()
    serialized_crop.save()


def _save_farm_instance(farm):
    serialized_farm = FarmSerializer(data=farm)
    serialized_farm.is_valid()
    farm_instance = serialized_farm.save()
    return farm_instance
