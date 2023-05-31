# Generated by Django 4.2 on 2023-05-31 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customuser_nim_alter_customuser_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('sas', 'SAS'), ('dininghall', 'Dining Hall'), ('student', 'Student'), ('library', 'Library'), ('laboratorium', 'Laboratorium')], default=None, max_length=20, null=True),
        ),
    ]