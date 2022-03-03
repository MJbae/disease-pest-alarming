from django.db import models

from forecasting.models.crops import Crop
from forecasting.models.farms import MediumCategoryAddress


class Forecasting(models.Model):
    date = models.DateField(blank=True)
    medium_category_address = models.ForeignKey(
        MediumCategoryAddress, on_delete=models.SET_NULL, null=True, db_column='medium_category_address_code'
    )
    crop = models.ForeignKey(
        Crop, on_delete=models.CASCADE, db_column='crop_code'
    )
    target = models.CharField(max_length=16, blank=True)

    def __str__(self):
        return f"{self.date}, {self.medium_category_address.__str__()}의 {self.crop.__str__()}에서 {self.target} 피해 발생"

    class Meta:
        ordering = ["-id"]
        db_table = 'forecasting'
