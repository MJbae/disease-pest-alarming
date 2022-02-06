from django.db import models


class Setting(models.Model):
    key = models.CharField(max_length=64)
    value = models.CharField(max_length=256)

    def __str__(self):
        return self.key

    class Meta:
        db_table = 'setting'
        ordering = ['-id']
