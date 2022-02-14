from rest_framework import serializers

from forecasting.models import Forecasting, Crop, ProducingCrop, Farm


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


class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = (
            "code",
            "name",
        )


class ProducingCropSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProducingCrop
        fields = (
            "pk",
            "farm",
            "crop",
            "is_in_house",
        )


class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = (
            "pk",
            "owner",
            "large_category_address",
            "medium_category_address",
        )
