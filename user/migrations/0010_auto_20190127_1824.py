# Generated by Django 2.1.5 on 2019-01-27 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='pic',
            field=models.FileField(default='/profile.png', null=True, upload_to=''),
        ),
    ]
