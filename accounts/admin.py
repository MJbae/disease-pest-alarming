from django.contrib import admin
from .models import User, Setting


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    pass
