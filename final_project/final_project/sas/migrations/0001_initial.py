# Generated by Django 4.2 on 2023-07-11 15:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attendee',
            fields=[
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='table_classes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_code', models.CharField(max_length=10)),
                ('class_name', models.CharField(max_length=75)),
                ('class_day', models.CharField(choices=[('monday', 'monday'), ('tuesday', 'tuesday'), ('wednesday', 'wednesday'), ('thursday', 'thursday'), ('friday', 'friday')], default='', max_length=9)),
                ('class_start_time', models.TimeField(default=datetime.time(9, 0))),
                ('class_end_time', models.TimeField(default=datetime.time(9, 0))),
                ('attendees', models.ManyToManyField(to='sas.attendee')),
            ],
        ),
    ]
