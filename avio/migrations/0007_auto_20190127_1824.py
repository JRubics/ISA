# Generated by Django 2.1.5 on 2019-01-27 18:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('avio', '0006_auto_20190123_1845'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='seat',
            unique_together={('seat_number', 'seat_type')},
        ),
    ]