from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import LeaveRequest

@login_required
def apply_leave(request):
    if request.method == 'POST':
        leave_type = request.POST.get('leave_type')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        reason = request.POST.get('reason')
        
        LeaveRequest.objects.create(
            user=request.user,
            leave_type=leave_type,
            start_date=start_date,
            end_date=end_date,
            reason=reason
        )
        messages.success(request, 'Leave request submitted successfully.')
        return redirect('dashboard')
        
    return render(request, 'leave/apply_leave.html')

@login_required
def approve_leave(request, leave_id):
    leave = get_object_or_404(LeaveRequest, id=leave_id)
    action = request.POST.get('action')
    
    if request.user.role == 'TL' and leave.status == 'Pending TL':
        if action == 'approve':
            leave.status = 'Pending HR'
            leave.tl_approved_by = request.user
            messages.success(request, 'Leave approved by TL, forwarded to HR.')
        elif action == 'reject':
            leave.status = 'Rejected'
            messages.error(request, 'Leave rejected by TL.')
        leave.save()
            
    elif request.user.role == 'HR' and leave.status == 'Pending HR':
        if action == 'approve':
            leave.status = 'Approved'
            leave.hr_approved_by = request.user
            messages.success(request, 'Leave fully approved by HR.')
        elif action == 'reject':
            leave.status = 'Rejected'
            messages.error(request, 'Leave rejected by HR.')
        leave.save()
        
    return redirect('dashboard')
