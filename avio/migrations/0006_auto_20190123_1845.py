# Generated by Django 2.1.5 on 2019-01-23 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avio', '0005_auto_20190123_1821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seat',
            name='seat_type',
            field=models.CharField(choices=[('B', 'Business seats'), ('O', 'Out of order'), ('F', 'First class seats'), ('E', 'Economy seats')], max_length=1),
        ),
    ]
