from rest_framework.viewsets import ModelViewSet

from forecasting.models import Forecasting
from forecasting.serializers import ForecastingSerializer


class ForecastingViewSet(ModelViewSet):
    queryset = Forecasting.objects.all()
    serializer_class = ForecastingSerializer
