from django.contrib import admin
from .models import Forecasting, Address, Crop


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    pass


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass


@admin.register(Forecasting)
class ForecastingAdmin(admin.ModelAdmin):
    pass
