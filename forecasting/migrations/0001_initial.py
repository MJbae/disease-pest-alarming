# Generated by Django 3.1.14 on 2022-02-06 06:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Crop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=13)),
                ('code', models.CharField(max_length=13)),
            ],
            options={
                'db_table': 'crop',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Farm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=13)),
                ('large_category_address', models.CharField(blank=True, choices=[('Seoul', '서울특별시'), ('Gyeonggi-do', '경기도')], max_length=15)),
                ('medium_category_address', models.CharField(blank=True, choices=[('Hwaseong-si', '화성시'), ('Suwon-si', '수원시'), ('Seongnam-si', '성남시'), ('Anyang-si', '안양시')], max_length=15)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='farm_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'farm',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Forecasting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sigungu_code', models.CharField(blank=True, max_length=16)),
                ('sigungu_name', models.CharField(blank=True, max_length=16)),
                ('crop_name', models.CharField(blank=True, max_length=16)),
                ('crop_code', models.CharField(blank=True, max_length=16)),
                ('target', models.CharField(blank=True, max_length=16)),
                ('susceptibility', models.FloatField()),
                ('generated_area', models.FloatField()),
                ('area_ratio', models.FloatField()),
                ('damage_rate', models.FloatField()),
            ],
            options={
                'db_table': 'forecasting',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ProducingCrop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_in_house', models.BooleanField(default=False)),
                ('crop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='producing_crop_set', to='forecasting.crop')),
                ('farm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='producing_crop_set', to='forecasting.farm')),
            ],
            options={
                'db_table': 'producing_crop',
                'ordering': ['-id'],
            },
        ),
    ]