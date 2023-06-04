from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('sas', 'SAS'),
        ('dininghall', 'Dining Hall'),
        ('student', 'Student'),
        ('library', 'Library'),
        ('laboratorium', 'Laboratorium'),
    ]
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150)
    nim = models.IntegerField(null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True)

    class Meta:
        # Remove 'groups' and 'user_permissions' fields
        managed = True
        default_permissions = ()
        permissions = ()
