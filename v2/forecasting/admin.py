from django.contrib import admin
from .models import Forecasting, Address, Crop, User, ProducingCrop, Farm


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    pass


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass


@admin.register(Forecasting)
class ForecastingAdmin(admin.ModelAdmin):
    pass


@admin.register(ProducingCrop)
class ProducingCropAdmin(admin.ModelAdmin):
    pass


@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    pass
