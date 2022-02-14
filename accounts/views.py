from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView
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
        print(f'password: {raw_password}')
        print(f'username: {hashed_password}')
        serializer.save(password=hashed_password)
