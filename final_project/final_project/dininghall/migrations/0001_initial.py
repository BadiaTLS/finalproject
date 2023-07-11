# Generated by Django 4.2 on 2023-07-11 15:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='table_booking_dininghall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recommended_time', models.TimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='table_session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('name', models.CharField(choices=[('Breakfast', 'Breakfast'), ('Lunch', 'Lunch'), ('Dinner', 'Dinner')], max_length=10)),
                ('menu', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='table_time',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField()),
                ('seat_limit', models.IntegerField()),
                ('available_seat', models.IntegerField(null=True)),
                ('session_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dininghall.table_session')),
            ],
        ),
        migrations.CreateModel(
            name='table_live_booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arrival_time', models.TimeField()),
                ('served_time', models.TimeField()),
                ('depart_time', models.TimeField()),
                ('bookings_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dininghall.table_booking_dininghall')),
            ],
        ),
        migrations.AddField(
            model_name='table_booking_dininghall',
            name='session_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dininghall.table_session'),
        ),
        migrations.AddField(
            model_name='table_booking_dininghall',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
