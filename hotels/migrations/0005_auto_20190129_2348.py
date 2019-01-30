# Generated by Django 2.1.3 on 2019-01-29 22:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0004_auto_20190129_1833'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotelreservation',
            name='rooms_charge',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0, 'Charge cannot be negative')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hotelreservation',
            name='services_charge',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0, 'Charge cannot be negative')]),
            preserve_default=False,
        ),
    ]