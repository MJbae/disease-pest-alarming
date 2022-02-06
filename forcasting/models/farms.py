from django.db import models

from backend.settings.common import AUTH_USER_MODEL
from forcasting.models.choices import LargeCategoryAddressChoices, MediumCategoryAddressChoices


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
