from django.db import models


class Forecasting(models.Model):
    sigungu_code = models.CharField(max_length=16, blank=True)
    sigungu_name = models.CharField(max_length=16, blank=True)
    crop_name = models.CharField(max_length=16, blank=True)
    crop_code = models.CharField(max_length=16, blank=True)
    target = models.CharField(max_length=16, blank=True)

    def __str__(self):
        return f"'{self.crop_name} in {self.sigungu_name} damaged by {self.target}"

    class Meta:
        ordering = ["-id"]
        db_table = 'forecasting'
