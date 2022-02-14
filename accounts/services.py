from forecasting.models import Crop
from forecasting.serializers import FarmSerializer, ProducingCropSerializer


def save_nested_models_in_new_user(farms, user_id):
    for farm in farms:
        farm["owner"] = user_id
        crops = farm.get("producing_crops")

        serialized_farm = FarmSerializer(data=farm)
        serialized_farm.is_valid()
        farm_instance = serialized_farm.save()

        for crop in crops:
            crop_name = crop.get("name")
            crop["farm"] = farm_instance.pk
            crop_code = Crop.objects.get(name=crop_name).code
            crop["crop"] = crop_code
            del (crop['name'])

            serialized_crop = ProducingCropSerializer(data=crop)
            serialized_crop.is_valid()
            serialized_crop.save()
