from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView

from forecasting.models import Crop
from forecasting.serializers import FarmSerializer, ProducingCropSerializer
from .serializers import SignupSerializer
from .services import save_nested_models_in_new_user


class SignupView(CreateAPIView):
    model = get_user_model()
    serializer_class = SignupSerializer
    permission_classes = [
        AllowAny,
    ]

    def perform_create(self, serializer):
        hashed_password = self._make_hashed_password(serializer)
        username = serializer.save(password=hashed_password)
        user_id = self._get_user_id(username)
        farms = self.request.data.get("farms")

        save_nested_models_in_new_user(farms, user_id)

    def _get_user_id(self, username):
        user = get_user_model().objects.get(username=username)
        user_id = user.id
        return user_id

    def _make_hashed_password(self, serializer):
        raw_password = serializer.validated_data.get("password")
        hashed_password = make_password(raw_password)
        return hashed_password
