from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('QC', 'QC'),
        ('TL', 'Team Leader'),
        ('HR', 'HR'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='QC')

    def __str__(self):
        return f"{self.username} ({self.role})"
