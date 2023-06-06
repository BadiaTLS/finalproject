from django.db import models
from datetime import time
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class table_students_information(models.Model):
    nim = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    study_program = models.CharField(max_length=10)
    batch_year = models.SmallIntegerField()
    username = models.CharField(max_length=50)
    email = models.EmailField(null=True)
    password = models.CharField(max_length=64)

class table_classes(models.Model):
    monday = "Monday"
    tuesday = "Tuesday"
    wednesday = "Wednesday"
    thursday = "Thursday"
    friday = "Friday"
    days = [
        (monday, "Monday"),
        (tuesday, "Tuesday"),
        (wednesday, "Wednesday"),
        (thursday, "Thursday"),
        (friday, "Friday")
    ]
    class_code = models.CharField(max_length=10, primary_key=True)
    class_name = models.CharField(max_length=75)
    class_day = models.CharField(max_length=9, choices=days, default=monday)
    class_start_time = models.TimeField(default=time(9,0))
    class_end_time = models.TimeField(default=time(9,0))
    attendees = models.ForeignKey(User, on_delete=models.CASCADE)
