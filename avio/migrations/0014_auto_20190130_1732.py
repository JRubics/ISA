# Generated by Django 2.1.5 on 2019-01-30 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avio', '0013_auto_20190130_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='price',
            field=models.FloatField(null=True),
        ),
    ]