# Generated by Django 2.1.5 on 2019-01-23 22:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('avio', '0006_auto_20190123_1845'),
        ('user', '0005_profile_bonus'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='avio_admin',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='avio.AvioCompany'),
        ),
    ]
