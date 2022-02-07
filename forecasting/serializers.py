from rest_framework import serializers

from forecasting.models import Forecasting


class ForecastingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forecasting
        fields = (
            "id",
            "date",
            "sigungu_code",
            "sigungu_name",
            "crop_name",
            "crop_code",
            "target",
        )
