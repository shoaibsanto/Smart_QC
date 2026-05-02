from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'factory', 'timestamp', 'latitude', 'longitude')
    list_filter = ('factory', 'timestamp')
    search_fields = ('user__username', 'factory__name')
