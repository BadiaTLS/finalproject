# Generated by Django 4.2 on 2023-07-10 17:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dininghall', '0003_rename_live_bookings_table_live_bookings'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='table_live_bookings',
            new_name='table_live_booking',
        ),
    ]