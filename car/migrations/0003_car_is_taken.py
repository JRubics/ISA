# Generated by Django 2.1.2 on 2019-01-09 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0002_branchoffice'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='is_taken',
            field=models.BooleanField(default=1),
        ),
    ]
