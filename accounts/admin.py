from django.contrib import admin
from .models import User
from .models.crops import Crop, ProducingCrop
from .models.users import Farm


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    pass


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    pass


@admin.register(ProducingCrop)
class ProducingCropAdmin(admin.ModelAdmin):
    pass
