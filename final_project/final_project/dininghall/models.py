from django.db import models

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
    limit = models.IntegerField()
    available = models.IntegerField(null=True)
    
class table_time(models.Model):
    time = models.TimeField()

    def __str__(self):
        return f"{self.time}"

class table_booking_dininghall(models.Model):
    students_nim = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    time_booked = models.TimeField()
    menu = models.ForeignKey(table_menu, on_delete=models.CASCADE)
    available = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)