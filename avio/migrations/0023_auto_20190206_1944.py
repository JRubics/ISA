# Generated by Django 2.1.5 on 2019-02-06 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avio', '0022_auto_20190206_0047'),
    ]

    operations = [
        migrations.AddField(
            model_name='packagereservation',
            name='city',
            field=models.CharField(max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='packagereservation',
            name='country',
            field=models.CharField(max_length=40),
            preserve_default=False,
        ),
    ]
