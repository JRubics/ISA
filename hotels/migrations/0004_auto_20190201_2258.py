# Generated by Django 2.1.5 on 2019-02-01 22:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hotels', '0003_hotelrate'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoomRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_rate', models.PositiveIntegerField()),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotels.HotelReservation')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotels.HotelRoom')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='hotelrate',
            name='rooms',
        ),
    ]