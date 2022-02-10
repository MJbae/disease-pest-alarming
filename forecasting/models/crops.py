from django.db import models

from forecasting.models import Farm


class Crop(models.Model):
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
        db_table = 'crop'


class ProducingCrop(models.Model):
    farm = models.ForeignKey(
        Farm, related_name="producing_crop_set", on_delete=models.CASCADE
    )
    crop = models.ForeignKey(
        Crop, related_name="producing_crop_set", on_delete=models.CASCADE
    )
    is_in_house = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.farm.__str__()} {self.crop.name}"

    class Meta:
        ordering = ["-id"]
        db_table = 'producing_crop'
