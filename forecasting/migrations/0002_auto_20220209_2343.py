# Generated by Django 3.1.14 on 2022-02-09 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forecasting', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='crop',
            options={'ordering': ['-code']},
        ),
        migrations.RemoveField(
            model_name='crop',
            name='id',
        ),
        migrations.AlterField(
            model_name='crop',
            name='code',
            field=models.CharField(max_length=8, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='crop',
            name='name',
            field=models.CharField(max_length=16),
        ),
    ]