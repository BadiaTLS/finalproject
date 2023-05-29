from django.db import models
from final_project.students.models import table_students_information
from datetime import datetime
from django.core.exceptions import ValidationError

# Create your models here.
class table_staff_information(models.Model):
    name = models.CharField(max_length=50)
    position = models.CharField(max_length=20)
    username = models.CharField(max_length=50)
    email = models.EmailField(null=True)
    password = models.CharField(max_length=64)

class table_menu(models.Model):
    breakfast = "Breakfast"
    lunch = "Lunch"
    dinner = "Dinner"
    options = [
        (breakfast, "Breakfast"),
        (lunch, "Lunch"),
        (dinner, "Dinner")
    ]
    date = models.DateField()
    session = models.CharField(max_length=10, choices=options)
    menu = models.TextField()
    vacancy = models.IntegerField(null=True)
    
class table_time(models.Model):
    time = models.TimeField()

    def __str__(self):
        return f"{self.time}"

class table_booking_dininghall(models.Model):
    students_nim = models.ManyToManyField(table_students_information)
    time_booked = models.TimeField()
    menu = models.ForeignKey(table_menu, on_delete=models.CASCADE, null=True)
    vacancy = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)