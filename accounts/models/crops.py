from django.db import models
from users import Farm


class Crop(models.Model):
    name = models.CharField(
        max_length=13,
    )
    code = models.CharField(
        max_length=13,
    )


class ProducingCrop(models.Model):
    farm = models.ForeignKey(
        Farm, related_name="producing_crop_set", on_delete=models.CASCADE
    )
    crop = models.ForeignKey(
        Crop, related_name="producing_crop_set", on_delete=models.CASCADE
    )
    is_in_house = models.BooleanField(default=False)
