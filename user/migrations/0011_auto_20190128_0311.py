# Generated by Django 2.1.5 on 2019-01-28 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_auto_20190127_1824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='pic',
            field=models.FileField(default='/profile.png', upload_to=''),
        ),
    ]