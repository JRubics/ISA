# Generated by Django 2.1.5 on 2019-01-23 16:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('avio', '0003_auto_20190123_1658'),
    ]

    operations = [
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure_date', models.DateTimeField(verbose_name='departure time')),
                ('arrival_date', models.DateTimeField(verbose_name='arrival time')),
                ('distance', models.IntegerField()),
                ('base_price', models.IntegerField()),
                ('arrival_airport', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='arrival_airport', to='avio.Airport')),
                ('arrival_city', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='arrival_city', to='avio.City')),
                ('avio_company', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='avio.AvioCompany')),
                ('departure_airport', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='departure_airport', to='avio.Airport')),
                ('departure_city', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='departure_city', to='avio.City')),
            ],
        ),
        migrations.CreateModel(
            name='FlightLeg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arrival_date', models.DateTimeField(verbose_name='arrival time')),
                ('departure_date', models.DateTimeField(verbose_name='departure time')),
                ('airport', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='avio.Airport')),
                ('flight', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='avio.Flight')),
            ],
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_number', models.IntegerField()),
                ('seat_status', models.CharField(choices=[('T', 'Taken seats'), ('F', 'Free seat'), ('P', 'Promotion seat')], max_length=1)),
                ('seat_type', models.CharField(choices=[('B', 'Business seats'), ('F', 'First class seats'), ('E', 'Economy seats')], max_length=1)),
                ('price_factor', models.FloatField(default=1)),
                ('flight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='avio.Flight')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(verbose_name='time of ticket creation')),
                ('status', models.IntegerField()),
                ('flight', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='avio.Flight')),
                ('seat', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='avio.Seat')),
            ],
        ),
    ]
