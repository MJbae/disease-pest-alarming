from django.contrib.auth import get_user_model
from rest_framework_jwt.utils import jwt_decode_handler
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import ParseError

from backend.settings.common import SECRET_KEY
from forecasting.models import Forecasting
from forecasting.serializers import ForecastingSerializer
from forecasting.tasks import c_catch_latest_forecasting


class ForecastingViewSet(ModelViewSet):
    """
        Temporary Using API ViewSet in order to test forecasting data
    """
    queryset = Forecasting.objects.all()
    serializer_class = ForecastingSerializer


@api_view(["GET"])
def update_forecasting(request):
    """
        API View that immediately act on periodic work of catching the latest forecasting
    """
    jwt = _get_jwt_from_header(request)
    user_id = _get_user_id_from_jwt(jwt)

    try:
        user = get_user_model().objects.get(id=user_id)

        if user.is_staff is False:
            raise ParseError(detail="권한이 없는 사용자입니다.")

        c_catch_latest_forecasting.delay()
    except get_user_model().ObjectDoesNotExist:
        raise ParseError(detail="알 수 없는 사용자입니다.")
    except Exception:
        raise ParseError(detail="알 수 없는 원인으로 예찰정보 전송에 실패했습니다.")
    return Response(status=status.HTTP_200_OK)


def _get_jwt_from_header(request):
    authorization_header = request.META.get('HTTP_AUTHORIZATION')
    jwt = authorization_header[4:]
    return jwt


def _get_user_id_from_jwt(jwt):
    payload = jwt_decode_handler(jwt)
    return payload.get('user_id')
