# Generated by Django 2.1.5 on 2019-01-09 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0003_car_is_taken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='is_taken',
            field=models.BooleanField(default=0),
        ),
    ]
