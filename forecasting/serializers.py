from rest_framework import serializers

from forecasting.models import Forecasting


class ForecastingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forecasting
        fields = "__all__"
