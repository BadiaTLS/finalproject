from django.db import models

class table_session(models.Model):
    breakfast = "Breakfast"
    lunch = "Lunch"
    dinner = "Dinner"
    options = [
        (breakfast, "Breakfast"),
        (lunch, "Lunch"),
        (dinner, "Dinner")
    ]
    date = models.DateField()
    name = models.CharField(max_length=10, choices=options)
    menu = models.TextField()
    
class table_time(models.Model):
    time = models.TimeField()
    session_id = models.ForeignKey(table_session, on_delete=models.CASCADE)
    seat_limit = models.IntegerField()
    available_seat = models.IntegerField(null=True)
    
    def __str__(self):
        return f"{self.time}"

class table_booking_dininghall(models.Model):
    user_id = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    session_id = models.ForeignKey(table_session, on_delete=models.CASCADE)
    recommended_time = models.TimeField()    
    created_at = models.DateTimeField(auto_now_add=True)

class table_live_booking(models.Model):
    arrival_time = models.TimeField()
    served_time = models.TimeField()
    depart_time = models.TimeField()
    bookings_id = models.ForeignKey(table_booking_dininghall, on_delete=models.CASCADE, null=True)
