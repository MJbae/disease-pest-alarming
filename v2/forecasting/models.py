from django.db import models


# TODO: sqlalchemy 추후 도입
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
        db_table = 'crop'
        ordering = ["-code"]


class Address(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(
        max_length=16,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-code"]
        db_table = 'address'


class Forecasting(models.Model):
    date = models.DateField(blank=True)
    address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, db_column='address_code'
    )
    crop = models.ForeignKey(
        Crop, on_delete=models.CASCADE, db_column='crop_code'
    )
    target = models.CharField(max_length=16, blank=True)

    class Meta:
        ordering = ["-id"]
        db_table = 'forecasting'
