from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Attendance
from factories.models import Factory
from datetime import date
import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000 # Radius of earth in meters
    phi_1 = math.radians(lat1)
    phi_2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2.0)**2 + math.cos(phi_1) * math.cos(phi_2) * math.sin(delta_lambda / 2.0)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@login_required
def mark_attendance(request):
    factories = Factory.objects.all()
    return render(request, 'attendance/mark_attendance.html', {'factories': factories})

@login_required
def submit_attendance(request):
    if request.method == 'POST':
        factory_id = request.POST.get('factory')
        lat = request.POST.get('latitude')
        lon = request.POST.get('longitude')
        
        if not lat or not lon:
            messages.error(request, 'Location is required. Please allow location access.')
            return redirect('mark_attendance')
            
        lat = float(lat)
        lon = float(lon)
        
        try:
            factory = Factory.objects.get(id=factory_id)
        except Factory.DoesNotExist:
            messages.error(request, 'Invalid factory selected.')
            return redirect('mark_attendance')
            
        # Check if already marked today for this factory
        today = date.today()
        already_marked = Attendance.objects.filter(
            user=request.user,
            factory=factory,
            timestamp__date=today
        ).exists()
        
        if already_marked:
            messages.error(request, f'You have already marked attendance for {factory.name} today.')
            return redirect('dashboard')
            
        distance = haversine(lat, lon, factory.latitude, factory.longitude)
        
        # Assume 200 meters radius
        if distance <= 200:
            Attendance.objects.create(
                user=request.user,
                factory=factory,
                latitude=lat,
                longitude=lon
            )
            messages.success(request, f'Attendance marked successfully at {factory.name}. Distance: {int(distance)}m')
        else:
            messages.error(request, f'You are too far from the factory to mark attendance. Distance: {int(distance)}m (Max allowed: 200m)')
            
    return redirect('dashboard')
