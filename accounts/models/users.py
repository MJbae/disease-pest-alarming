from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from accounts.models.choices import GenderChoices, LargeCategoryAddressChoices, MediumCategoryAddressChoices


class User(AbstractUser):
    gender = models.CharField(max_length=1, blank=True, choices=GenderChoices.choices)

    phone_number = models.CharField(
        max_length=13,
        blank=True,
        validators=[RegexValidator(r"^010-?[1-9]\d{3}-?\d{4}$")],
    )

    large_category_address = models.CharField(max_length=15, blank=True, choices=LargeCategoryAddressChoices.choices)
    medium_category_address = models.CharField(max_length=15, blank=True, choices=MediumCategoryAddressChoices.choices)

    def get_full_name(self):
        return f"{self.last_name} {self.first_name}".strip()
