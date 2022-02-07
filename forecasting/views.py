from rest_framework.viewsets import ModelViewSet

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import ParseError

from forecasting.models import Forecasting
from forecasting.serializers import ForecastingSerializer
from forecasting.services.forecasting import catch_latest_forecasting


class ForecastingViewSet(ModelViewSet):
    queryset = Forecasting.objects.all()
    serializer_class = ForecastingSerializer


@api_view(["GET"])
def update_forecasting(request):
    try:
        catch_latest_forecasting()
    except Exception:  # TODO: 구체적인 Exception으로 변경할 것
        raise ParseError(detail="fail to update forecasting")

    return Response(status=status.HTTP_200_OK)
