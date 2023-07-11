# Generated by Django 4.2 on 2023-07-10 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='gender',
            field=models.CharField(choices=[('male', 'MALE'), ('female', 'FEMALE')], max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='major',
            field=models.CharField(choices=[('ibda', 'IBDA'), ('iee', 'IEE'), ('cfp', 'CFP'), ('asd', 'ASD'), ('bms', 'BMS'), ('scce', 'SCCE')], max_length=4, null=True),
        ),
    ]