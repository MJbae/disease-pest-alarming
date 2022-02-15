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
            response = requests.post(url=url, json=request_body)

            if response.status_code == 201:
                return redirect('index')

    return render(request, 'signup.html')
