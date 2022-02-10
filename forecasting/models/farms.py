from django.db import models

from backend.settings.common import AUTH_USER_MODEL
from forecasting.models.choices import LargeCategoryAddressChoices, MediumCategoryAddressChoices


class Farm(models.Model):
    owner = models.ForeignKey(
        AUTH_USER_MODEL, related_name="farm_set", on_delete=models.CASCADE
    )

    large_category_address = models.CharField(max_length=15, blank=True, choices=LargeCategoryAddressChoices.choices)
    medium_category_address = models.CharField(max_length=15, blank=True, choices=MediumCategoryAddressChoices.choices)

    def __str__(self):
        return f"{self.medium_category_address}의 {self.owner.__str__()}농장"

    class Meta:
        ordering = ["-id"]
        db_table = 'farm'
