from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    phone_number = models.CharField(
        max_length=13,
        blank=True,
        validators=[RegexValidator(r"^010-?[1-9]\d{3}-?\d{4}$")],
    )

    def get_full_name(self):
        return f"{self.last_name} {self.first_name}".strip()

    def __str__(self):
        return self.get_full_name()

    class Meta:
        ordering = ["-id"]
