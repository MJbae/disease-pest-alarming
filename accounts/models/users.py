from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from accounts.models.choices import LargeCategoryAddressChoices, MediumCategoryAddressChoices
from backend.settings.common import AUTH_USER_MODEL


class User(AbstractUser):
    phone_number = models.CharField(
        max_length=13,
        blank=True,
        validators=[RegexValidator(r"^010-?[1-9]\d{3}-?\d{4}$")],
    )

    def get_full_name(self):
        return f"{self.last_name} {self.first_name}".strip()

    def __str__(self):
        return self.get_full_name()

    class Meta:
        ordering = ["-id"]


class Farm(models.Model):
    owner = models.ForeignKey(
        AUTH_USER_MODEL, related_name="farm_set", on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=13,
        blank=True,
    )
    large_category_address = models.CharField(max_length=15, blank=True, choices=LargeCategoryAddressChoices.choices)
    medium_category_address = models.CharField(max_length=15, blank=True, choices=MediumCategoryAddressChoices.choices)

    def __str__(self):
        return f"{self.owner.__str__()}'s {self.name}"

    class Meta:
        ordering = ["-id"]
        db_table = 'farm'
