from django.db import models
from datetime import time
from django.contrib.auth import get_user_model

User = get_user_model()

class Attendee(models.Model):
    email = models.EmailField(primary_key=True)

    def __str__(self):
        return self.email

class table_classes(models.Model):
    monday = "monday"
    tuesday = "tuesday"
    wednesday = "wednesday"
    thursday = "thursday"
    friday = "friday"
    days = [
        (monday, "monday"),
        (tuesday, "tuesday"),
        (wednesday, "wednesday"),
        (thursday, "thursday"),
        (friday, "friday")
    ]
    class_code = models.CharField(max_length=10, primary_key=True)
    class_name = models.CharField(max_length=75)
    class_day = models.CharField(max_length=9, choices=days, default="")
    class_start_time = models.TimeField(default=time(9, 0))
    class_end_time = models.TimeField(default=time(9, 0))
    attendees = models.ManyToManyField(Attendee)
