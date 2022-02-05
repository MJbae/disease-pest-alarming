from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from accounts.models.choices import LargeCategoryAddressChoices, MediumCategoryAddressChoices
from backend import settings


class User(AbstractUser):
    phone_number = models.CharField(
        max_length=13,
        blank=True,
        validators=[RegexValidator(r"^010-?[1-9]\d{3}-?\d{4}$")],
    )

    def get_full_name(self):
        return f"{self.last_name} {self.first_name}".strip()


class Farm(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="farm_set", on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=13,
        blank=True,
    )
    large_category_address = models.CharField(max_length=15, blank=True, choices=LargeCategoryAddressChoices.choices)
    medium_category_address = models.CharField(max_length=15, blank=True, choices=MediumCategoryAddressChoices.choices)
