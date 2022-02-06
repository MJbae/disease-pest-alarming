from django.db import models


class LargeCategoryAddressChoices(models.TextChoices):
    SEOUL = "Seoul", "서울특별시"
    GYEONGGI = "Gyeonggi-do", "경기도",


class MediumCategoryAddressChoices(models.TextChoices):
    HWASEONG = "Hwaseong-si", "화성시"
    SUWON = "Suwon-si", "수원시"
    SEONGNAM = "Seongnam-si", "성남시"
    ANYANG = "Anyang-si", "안양시"
