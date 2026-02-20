from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.http import require_POST
from hr_module.models import Task, Attendance, Leave, LeaveBalance
from django.contrib import messages
from django.contrib.auth import get_user_model
from functools import wraps
from django.db.models import Q

User = get_user_model()

# Custom decorator to check if user is employee
# This ensures only employees can access employee views
def employee_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.role != 'Employee':
            messages.error(request, "Access denied. This page is only for employees")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required
@employee_required
def employee_dashboard(request):
    """
    Employee Dashboard View - Shows overview of tasks, attendance, leaves
    This function displays statistics and recent activities for the logged-in employee
    """
    user = request.user
    today = timezone.now().date()

    # Get today's attendance record
    attendance_today = Attendance.objects.filter(
        user=user, date=today
    ).first()

    # Calculate task statistics
    total_tasks = Task.objects.filter(assigned_to=user).count()
    pending_tasks = Task.objects.filter(
        assigned_to=user, status='Pending'
    ).count()
    
    completed_tasks = Task.objects.filter(
        assigned_to=user, status='Completed'
    ).count()

    # Find overdue tasks (due date passed but not completed)
    overdue_tasks = Task.objects.filter(
        assigned_to=user,
        due_date__lt=today
    ).exclude(status__in=['Completed', 'Cancelled']).count()

    # Get recent leave applications (last 5)
    recent_leaves = Leave.objects.filter(
        user=user
    ).order_by('-applied_at')[:5]

    # Get or create leave balance for current year
    try:
        leave_balance_obj = LeaveBalance.objects.get(user=user, year=today.year)
        total_leaves = leave_balance_obj.sick_leave + leave_balance_obj.casual_leave + leave_balance_obj.earned_leave
    except LeaveBalance.DoesNotExist:
        # Create leave balance if it doesn't exist (for new employees)
        leave_balance_obj = LeaveBalance.objects.create(user=user, year=today.year)
        total_leaves = 39  # Default: 12 sick + 12 casual + 15 earned

    # Calculate attendance statistics
    present_days = Attendance.objects.filter(
        user=user, status='Present'
    ).count()

    absent_days = Attendance.objects.filter(
        user=user, status='Absent'
    ).count()

    # Prepare context data for template
    context = {
        'user': user,
        'attendance_today': attendance_today,
        'total_tasks': total_tasks,
        'pending_tasks': pending_tasks,
        'completed_tasks': completed_tasks,
        'overdue_tasks': overdue_tasks,
        'recent_leaves': recent_leaves,
        'leave_balance': leave_balance_obj,
        'total_leaves': total_leaves,
        'present_days': present_days,
        'absent_days': absent_days,
    }

    return render(request, 'employee_module/dashboard.html', context)

@login_required
@employee_required
def employee_tasks(request):
    """
    Employee Tasks View - Shows all tasks assigned to the employee
    Allows filtering by status (All/Pending/In Progress/Completed)
    """
    # Get filter parameter from URL query string
    status_filter = request.GET.get('status', 'all')
    
    # Fetch all tasks assigned to current logged-in employee
    tasks = Task.objects.filter(assigned_to=request.user).order_by('-created_at')
    
    # Apply status filter if selected
    if status_filter != 'all':
        tasks = tasks.filter(status=status_filter)
    
    context = {
        'tasks': tasks,
        'status_filter': status_filter
    }
    return render(request, 'employee_module/tasks.html', context)

@login_required
@employee_required
def update_task_status(request, task_id):
    """
    Update Task Status View - Allows status transitions and file submission
    Pending → In Progress → Completed (one direction only)
    File submission required when completing task
    """
    # Get task ensuring it belongs to current employee
    task = get_object_or_404(Task, id=task_id, assigned_to=request.user)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        
        # Only allow certain status transitions (workflow validation)
        if task.status == 'Pending' and new_status == 'In Progress':
            task.status = 'In Progress'
            task.save()
            messages.success(request, "Task status updated to In Progress")
        elif task.status == 'In Progress' and new_status == 'Completed':
            # Check if file is uploaded
            submission_file = request.FILES.get('submission_file')
            if not submission_file:
                messages.error(request, "Please upload a file to complete the task")
                return redirect('employee:tasks')
            
            task.status = 'Completed'
            task.submission_file = submission_file
            task.completed_at = timezone.now()  # Record completion time
            task.save()
            messages.success(request, "Task marked as completed with submission file!")
        else:
            messages.warning(request, "Invalid status transition")
    
    return redirect('employee:tasks')

@login_required
@employee_required
def employee_attendance(request):
    """
    Employee Attendance View - Shows attendance history (read-only)
    HR marks attendance, employees can only view their records
    """
    # Get last 30 attendance records (most recent first)
    attendance_records = Attendance.objects.filter(
        user=request.user
    ).order_by('-date')[:30]

    # Calculate attendance statistics
    total_records = Attendance.objects.filter(user=request.user).count()
    present_count = Attendance.objects.filter(user=request.user, status='Present').count()
    
    # Calculate percentage (avoid division by zero)
    if total_records > 0:
        attendance_percentage = round((present_count / total_records) * 100, 2)
    else:
        attendance_percentage = 0

    context = {
        'attendance_records': attendance_records,
        'attendance_percentage': attendance_percentage,
        'total_records': total_records,
        'present_count': present_count
    }
    
    return render(request, 'employee_module/attendance.html', context)

@login_required
@employee_required
def employee_leave(request):
    """
    Employee Leave View - Shows leave balance and history
    Displays all leave applications with their status
    """
    # Get all leave applications for the logged-in employee (newest first)
    leaves = Leave.objects.filter(
        user=request.user
    ).order_by('-applied_at')

    # Get or create leave balance for current year
    today = timezone.now().date()
    try:
        leave_balance = LeaveBalance.objects.get(user=request.user, year=today.year)
    except LeaveBalance.DoesNotExist:
        # Auto-create if doesn't exist (for new employees or new year)
        leave_balance = LeaveBalance.objects.create(user=request.user, year=today.year)

    context = {
        'leaves': leaves,
        'leave_balance': leave_balance
    }

    return render(request, 'employee_module/leave.html', context)

@login_required
@employee_required
def apply_leave(request):
    """
    Apply for Leave View - Handles leave application submission
    Validates dates and checks for overlapping leaves
    """
    if request.method == 'POST':
        leave_type = request.POST.get('leave_type')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        reason = request.POST.get('reason')

        # Check if all fields are filled
        if not all([leave_type, start_date, end_date, reason]):
            messages.error(request, "All fields are required")
            return redirect('employee:leave')

        # Convert string dates to date objects for comparison
        from datetime import datetime
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        # Validate that end date is not before start date
        if start > end:
            messages.error(request, "End date cannot be before start date")
            return redirect('employee:leave')

        # Check for overlapping leaves (approved or pending)
        # We use Q objects for complex OR conditions
        overlapping = Leave.objects.filter(
            user=request.user,
            status__in=['Pending', 'Approved']
        ).filter(
            Q(start_date__lte=end) & Q(end_date__gte=start)
        )

        if overlapping.exists():
            messages.error(request, "You already have a leave request for this period")
            return redirect('employee:leave')

        # Create leave request with status as Pending
        Leave.objects.create(
            user=request.user,
            leave_type=leave_type,
            start_date=start,
            end_date=end,
            reason=reason,
            status='Pending'
        )

        messages.success(request, "Leave application submitted successfully!")
        return redirect('employee:leave')

    return redirect('employee:leave')

@login_required
@employee_required
def accept_task(request, task_id):
    """
    Accept Task View - Employee accepts the assigned task
    Only pending acceptance tasks can be accepted
    """
    task = get_object_or_404(Task, id=task_id, assigned_to=request.user)
    
    if task.acceptance_status == 'Pending':
        task.acceptance_status = 'Accepted'
        task.save()
        messages.success(request, f"Task '{task.title}' accepted successfully!")
    else:
        messages.warning(request, "This task has already been processed")
    
    return redirect('employee:tasks')

@login_required
@employee_required
def reject_task(request, task_id):
    """
    Reject Task View - Employee rejects the assigned task with reason
    Requires rejection reason to be provided
    """
    task = get_object_or_404(Task, id=task_id, assigned_to=request.user)
    
    if request.method == 'POST':
        reason = request.POST.get('rejection_reason')
        
        if not reason or not reason.strip():
            messages.error(request, "Please provide a reason for rejection")
            return redirect('employee:tasks')
        
        if task.acceptance_status == 'Pending':
            task.acceptance_status = 'Rejected'
            task.status = 'Rejected'
            task.rejection_reason = reason
            task.save()
            messages.success(request, f"Task '{task.title}' rejected")
        else:
            messages.warning(request, "This task has already been processed")
    
    return redirect('employee:tasks')

@login_required
@employee_required
def mark_attendance(request):
    """
    Mark Attendance View - Employee marks their own attendance
    HR will verify it later
    """
    if request.method == 'POST':
        today = timezone.now().date()
        check_in = request.POST.get('check_in_time')
        notes = request.POST.get('notes', '')
        
        # Check if attendance already marked for today
        existing = Attendance.objects.filter(user=request.user, date=today).first()
        if existing:
            messages.warning(request, "Attendance already marked for today")
            return redirect('employee:attendance')
        
        # Validate check-in time
        if not check_in:
            messages.error(request, "Please provide your check-in time")
            return redirect('employee:attendance')
        
        # Create attendance record (pending HR verification)
        Attendance.objects.create(
            user=request.user,
            date=today,
            status='Present',
            check_in_time=check_in,
            check_out_time=None,
            notes=notes,
            marked_by=request.user,
            is_verified=False  # Pending HR verification
        )
        
        messages.success(request, "Attendance marked successfully! Waiting for HR verification")
        return redirect('employee:attendance')
    
    return redirect('employee:attendance')

