from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validators=[username_validator],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can log into this admin site.'
    )
    is_active = models.BooleanField(
        'active',
        default=True,
        help_text=
        'Designates whether this user should be treated as active. '
        'Unselect this instead of deleting accounts.'
    )
    date_joined = models.DateTimeField('date joined', default=timezone.now)
    phone_number = models.CharField(
        max_length=13,
        unique=True,
        blank=True,
        validators=[RegexValidator(r"^010-?[1-9]\d{3}-?\d{4}$")],
    )

    email = models.EmailField('email address', blank=True)
    objects = UserManager()
    USERNAME_FIELD = 'username'

    def __str__(self):
        return super().__str__()

    class Meta:
        db_table = "user"
        ordering = ["-id"]


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


class Farm(models.Model):
    owner = models.ForeignKey(
        User, related_name="farm_set", on_delete=models.CASCADE
    )
    address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, db_column='large_category_address_code'
    )

    def __str__(self):
        return f"{self.address.__str__()}의 {self.owner.__str__()}농장"

    class Meta:
        ordering = ["-id"]
        db_table = 'farm'


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


class ProducingCrop(models.Model):
    farm = models.ForeignKey(
        Farm, related_name="producing_crop_set", on_delete=models.CASCADE
    )
    crop = models.ForeignKey(
        Crop, related_name="producing_crop_set", on_delete=models.CASCADE, db_column='crop_code'
    )
    is_in_house = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.farm.__str__()} {self.crop.name}"

    class Meta:
        db_table = 'producing_crop'
        ordering = ["-id"]


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
