from django.db import models


class LargeCategoryAddressChoices(models.TextChoices):
    GYEONGGI = "경기도", "경기도"


class MediumCategoryAddressChoices(models.TextChoices):
    HWASEONG = "화성시", "화성시"
    SUWON = "수원시", "수원시"
    SEONGNAM = "성남시", "성남시"
    ANYANG = "안양시", "안양시"
    GAPYEONG = "가평군", "가평군"
