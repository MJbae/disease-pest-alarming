from django.contrib import admin
from .models.crops import Crop, ProducingCrop
from .models.farms import Farm


@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    pass


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    pass


@admin.register(ProducingCrop)
class ProducingCropAdmin(admin.ModelAdmin):
    pass
