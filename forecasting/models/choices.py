from django.db import models


class LargeCategoryAddressChoices(models.TextChoices):
    SEOUL = "서울특별시", "서울특별시"
    GYEONGGI = "경기도", "경기도"


class MediumCategoryAddressChoices(models.TextChoices):
    HWASEONG = "화성시", "화성시"
    SUWON = "수원시", "수원시"
    SEONGNAM = "성남시", "성남시"
    ANYANG = "안양시", "안양시"
