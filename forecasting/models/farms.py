from django.db import models

from backend.settings.common import AUTH_USER_MODEL


class LargeCategoryAddress(models.Model):
    code = models.CharField(
        max_length=8, primary_key=True
    )
    name = models.CharField(
        max_length=16,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-code"]
        db_table = 'large_category_address'


class MediumCategoryAddress(models.Model):
    code = models.CharField(
        max_length=8, primary_key=True
    )
    name = models.CharField(
        max_length=16,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-code"]
        db_table = 'medium_category_address'


class Farm(models.Model):
    owner = models.ForeignKey(
        AUTH_USER_MODEL, related_name="farm_set", on_delete=models.CASCADE
    )
    large_category_address = models.ForeignKey(
        LargeCategoryAddress, on_delete=models.SET_NULL, null=True, db_column='large_category_address_code'
    )
    medium_category_address = models.ForeignKey(
        MediumCategoryAddress, on_delete=models.SET_NULL, null=True, db_column='medium_category_address_code'
    )

    def __str__(self):
        return f"{self.medium_category_address.__str__()}의 {self.owner.__str__()}농장"

    class Meta:
        ordering = ["-id"]
        db_table = 'farm'
