from django.db import models


class Crop(models.Model):
    name = models.CharField(
        max_length=13,
    )
    code = models.CharField(
        max_length=13,
    )
