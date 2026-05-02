from django.db import models
from users.models import CustomUser

class LeaveRequest(models.Model):
    LEAVE_TYPES = (
        ('Casual', 'Casual'),
        ('Sick', 'Sick'),
        ('Earned', 'Earned'),
        ('Other', 'Other'),
    )

    STATUS_CHOICES = (
        ('Pending TL', 'Pending TL'),
        ('Pending HR', 'Pending HR'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.CharField(max_length=50, choices=LEAVE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending TL')
    
    tl_approved_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='tl_approved_leaves')
    hr_approved_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='hr_approved_leaves')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.leave_type} ({self.status})"
