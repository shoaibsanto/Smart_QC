from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    user = request.user
    context = {'role': user.role}
    
    if user.role == 'QC':
        # Get recent attendance and leave status for QC
        context['attendances'] = user.attendances.all()[:5]
        context['leaves'] = user.leave_requests.all()[:5]
    elif user.role == 'TL':
        from leave.models import LeaveRequest
        context['pending_leaves'] = LeaveRequest.objects.filter(status='Pending TL')
    elif user.role == 'HR':
        from leave.models import LeaveRequest
        context['pending_leaves'] = LeaveRequest.objects.filter(status='Pending HR')
    elif user.role == 'Admin':
        from factories.models import Factory
        context['factories_count'] = Factory.objects.count()
        
    return render(request, 'dashboard.html', context)
