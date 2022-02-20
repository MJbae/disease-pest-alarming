from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect

import requests
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView

from backend.settings.common import BASE_URL
from forecasting.models import Crop
from forecasting.serializers import FarmSerializer, ProducingCropSerializer
from .serializers import SignupSerializer
from .services import save_nested_models_in_new_user
from .tasks import c_send_sms_to_new


class SignupView(CreateAPIView):
    """
    API View that receives a POST with a user info including farms and producing_crops
    """
    model = get_user_model()
    serializer_class = SignupSerializer
    permission_classes = [
        AllowAny,
    ]

    def perform_create(self, serializer):
        raw_password = serializer.validated_data.get("password")
        hashed_password = make_password(raw_password)

        username = serializer.save(password=hashed_password)
        user_id = self._get_user_id(username)
        farms = self.request.data.get("farms")

        save_nested_models_in_new_user(farms, user_id)

    def _get_user_id(self, username):
        user = get_user_model().objects.get(username=username)
        return user.id


def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        request_body = {}
        username = request.POST['UserName']
        password = request.POST['Password']
        confirm_password = request.POST['ConfirmPassword']
        phone_number = request.POST['PhoneNumber']
        large_category_address = request.POST['LargeCategoryAddress']
        medium_category_address = request.POST['MediumCategoryAddress']
        crop_name = request.POST['CropName']

        if password == confirm_password:
            request_body['username'] = username
            request_body['password'] = password
            request_body['phone_number'] = phone_number
            farms = [
                {
                    "producing_crops": [
                        {
                            "name": crop_name
                        }
                    ],
                    "large_category_address": large_category_address,
                    "medium_category_address": medium_category_address
                }
            ]

            request_body['farms'] = farms
            url = f"{BASE_URL}/api/v1/accounts/signup/"

            if get_user_model().objects.filter(is_staff=False).count() > 100:
                return redirect('index')

            try:  # TODO: 추후에 비동기로 처리하거나 wsgi에서 callback에 따른 이슈 해결법 찾기
                requests.post(url=url, json=request_body)
            except Exception:
                return redirect('index')
            finally:
                c_send_sms_to_new.delay(username, phone_number)
                return redirect('index')

    return render(request, 'signup.html')
