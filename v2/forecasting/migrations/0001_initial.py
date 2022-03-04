# Generated by Django 3.1.14 on 2022-03-04 07:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('code', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=16)),
            ],
            options={
                'db_table': 'address',
                'ordering': ['-code'],
            },
        ),
        migrations.CreateModel(
            name='Crop',
            fields=[
                ('code', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=16)),
            ],
            options={
                'db_table': 'crop',
                'ordering': ['-code'],
            },
        ),
        migrations.CreateModel(
            name='Forecasting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True)),
                ('target', models.CharField(blank=True, max_length=16)),
                ('address', models.ForeignKey(db_column='address_code', null=True, on_delete=django.db.models.deletion.SET_NULL, to='forecasting.address')),
                ('crop', models.ForeignKey(db_column='crop_code', on_delete=django.db.models.deletion.CASCADE, to='forecasting.crop')),
            ],
            options={
                'db_table': 'forecasting',
                'ordering': ['-id'],
            },
        ),
    ]
