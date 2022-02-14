from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView

from forecasting.models import Crop
from forecasting.serializers import FarmSerializer, ProducingCropSerializer
from .serializers import SignupSerializer


class SignupView(CreateAPIView):
    model = get_user_model()
    serializer_class = SignupSerializer
    permission_classes = [
        AllowAny,
    ]

    def perform_create(self, serializer):
        raw_password = serializer.validated_data.get("password")
        hashed_password = make_password(raw_password)
        username = serializer.save(password=hashed_password)
        user = get_user_model().objects.get(username=username)
        farms = self.request.data.get("farms")

        for farm in farms:
            farm["owner"] = user.id
            crops = farm.get("producing_crops")

            serialized_farm = FarmSerializer(data=farm)
            serialized_farm.is_valid()
            farm_instance = serialized_farm.save()

            for crop in crops:
                crop_name = crop.get("name")
                crop["farm"] = farm_instance.pk
                crop_code = Crop.objects.get(name=crop_name).code
                crop["crop"] = crop_code
                del(crop['name'])

                serialized_crop = ProducingCropSerializer(data=crop)
                serialized_crop.is_valid()
                serialized_crop.save()
