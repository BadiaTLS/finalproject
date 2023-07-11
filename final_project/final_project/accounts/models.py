from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('sas', 'SAS'),
        ('dininghall', 'Dining Hall'),
        ('student', 'Student'),
        ('library', 'Library'),
        ('laboratorium', 'Laboratorium'),
        ('dosen', 'Dosen'),
    ]
    GENDERS = [
        ('male', 'MALE'),
        ('female', 'FEMALE'),
    ]
    MAJORS = [
        ('ibda', 'IBDA'),
        ('iee', 'IEE'),
        ('cfp', 'CFP'),
        ('asd', 'ASD'),
        ('bms', 'BMS'),
        ('scce', 'SCCE'),
    ]
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True)
    gender = models.CharField(max_length=6, choices=GENDERS, null=True)
    major = models.CharField(max_length=4, choices=MAJORS, null=True)

    class Meta:
        # Remove 'groups' and 'user_permissions' fields
        managed = True
        default_permissions = ()
        permissions = ()
