# Generated by Django 2.1.2 on 2018-11-05 18:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20181101_1334'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'permissions': (('is_car_admin', 'Is car admin'), ('is_hotel_admin', 'Is hotel admin'), ('is_flight_admin', 'Is flight admin'))},
        ),
    ]