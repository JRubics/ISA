# Generated by Django 2.1.3 on 2019-01-29 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0006_auto_20190129_2354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotelshoppingcart',
            name='rooms_charge',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='hotelshoppingcart',
            name='services_charge',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
