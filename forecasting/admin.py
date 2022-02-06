from django.contrib import admin
from .models.crops import Crop, ProducingCrop
from .models.farms import Farm
from .models.forecasting import Forecasting


@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    pass


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    pass


@admin.register(ProducingCrop)
class ProducingCropAdmin(admin.ModelAdmin):
    pass


@admin.register(Forecasting)
class ForecastingAdmin(admin.ModelAdmin):
    pass
