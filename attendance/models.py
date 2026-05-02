from django.db import models
from users.models import CustomUser
from factories.models import Factory

class Attendance(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='attendances')
    factory = models.ForeignKey(Factory, on_delete=models.CASCADE, related_name='attendances')
    timestamp = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        # Prevents multiple check-ins per user per factory per day if we enforce it. 
        # But for 'per day', we need a DateField or validation in the save/form.
        # We will add logic in the view to enforce "once per factory per visit".
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} at {self.factory.name} on {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
