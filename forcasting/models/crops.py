from django.db import models


class Crop(models.Model):
    name = models.CharField(
        max_length=13,
    )
    code = models.CharField(
        max_length=13,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-id"]
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
        return f"{self.farm.name}'s {self.crop.name}"

    class Meta:
        ordering = ["-id"]
        db_table = 'producing_crop'
