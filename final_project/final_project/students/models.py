from django.db import models

# Create your models here.
class table_students_information(models.Model):
    nim = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    study_program = models.CharField(max_length=10)
    batch_year = models.SmallIntegerField()
    username = models.CharField(max_length=50)
    email = models.EmailField(null=True)
    password = models.CharField(max_length=64)
