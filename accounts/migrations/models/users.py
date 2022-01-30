from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from accounts.migrations.models.choices import GenderChoices


class User(AbstractUser):
    gender = models.CharField(max_length=1, blank=True, choices=GenderChoices.choices)

    phone_number = models.CharField(
        max_length=13,
        blank=True,
        validators=[RegexValidator(r"^010-?[1-9]\d{3}-?\d{4}$")],
    )

    first_address = models.CharField()
    last_address = models.CharField()

    def get_full_name(self):
        return f"{self.last_name} {self.first_name}".strip()
