from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models import Count, Q, Sum
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from datetime import date, timedelta, datetime
import csv
import json

from .models import Attendance, Leave, Task, LeaveBalance
from .forms import AttendanceForm, BulkAttendanceForm, LeaveForm, LeaveApprovalForm, TaskForm, TaskStatusForm
from admin_panel.models import AuditLog

User = get_user_model()

# Helper function to parse date from string in various formats
def parse_date(date_string):
    """Parse date from string in various formats, return YYYY-MM-DD string"""
    if not date_string:
        return date.today().strftime('%Y-%m-%d')
    
    if isinstance(date_string, date):
        return date_string.strftime('%Y-%m-%d')
    
    # Try to parse the date
    try:
        # Try YYYY-MM-DD format first
        parsed = datetime.strptime(str(date_string), '%Y-%m-%d').date()
        return parsed.strftime('%Y-%m-%d')
    except ValueError:
        try:
            # Try other common formats
            parsed = datetime.strptime(str(date_string), '%m/%d/%Y').date()
            return parsed.strftime('%Y-%m-%d')
        except ValueError:
            # If all fails, return today
            return date.today().strftime('%Y-%m-%d')

# Helper function to log actions
def log_action(user, action, details, request):
    ip = request.META.get('REMOTE_ADDR')
    AuditLog.objects.create(user=user, action=action, details=details, ip_address=ip)

# HR dashboard
@login_required
def hr_dashboard(request):
    if request.user.role != 'HR':
        messages.error(request, 'You do not have permission to access HR dashboard.')
        return redirect('login')
    
    # Stats
    total_employees = User.objects.filter(role='Employee', is_active=True).count()
    today = date.today()
    
    # Attendance stats for today
    present_today = Attendance.objects.filter(date=today, status='Present').count()
    absent_today = Attendance.objects.filter(date=today, status='Absent').count()
    on_leave_today = Attendance.objects.filter(date=today, status='On Leave').count()
    
    # Leave requests
    pending_leaves = Leave.objects.filter(status='Pending').count()
    approved_leaves = Leave.objects.filter(status='Approved', start_date__lte=today, end_date__gte=today).count()
    
    # Tasks
    pending_tasks = Task.objects.filter(status='Pending').count()
    overdue_tasks = Task.objects.filter(status__in=['Pending', 'In Progress'], due_date__lt=today).count()
    
    # Recent leave requests
    recent_leaves = Leave.objects.filter(status='Pending').order_by('-applied_at')[:5]
    
    # Recent tasks
    recent_tasks = Task.objects.filter(assigned_by=request.user).order_by('-created_at')[:5]
    
    # Department wise attendance (for chart)
    departments = User.objects.filter(role='Employee', is_active=True).values('department').annotate(count=Count('id'))
    dept_labels = [d['department'] or 'Not Assigned' for d in departments]
    dept_counts = [d['count'] for d in departments]
    
    context = {
        'total_employees': total_employees,
        'present_today': present_today,
        'absent_today': absent_today,
        'on_leave_today': on_leave_today,
        'pending_leaves': pending_leaves,
        'approved_leaves': approved_leaves,
        'pending_tasks': pending_tasks,
        'overdue_tasks': overdue_tasks,
        'recent_leaves': recent_leaves,
        'recent_tasks': recent_tasks,
        'dept_labels': json.dumps(dept_labels),
        'dept_counts': json.dumps(dept_counts),
    }
    
    return render(request, 'hr_module/dashboard.html', context)

# Attendance list
@login_required
def attendance_list(request):
    if request.user.role != 'HR':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('login')
    
    # Filters
    date_filter = request.GET.get('date', '')
    status_filter = request.GET.get('status', '')
    department_filter = request.GET.get('department', '')
    search = request.GET.get('search', '')
    
    attendances = Attendance.objects.select_related('user', 'marked_by').all()
    
    if date_filter:
        attendances = attendances.filter(date=date_filter)
    else:
        # Default to today
        date_filter = date.today().strftime('%Y-%m-%d')
        attendances = attendances.filter(date=date_filter)
    
    if status_filter:
        attendances = attendances.filter(status=status_filter)
    
    if department_filter:
        attendances = attendances.filter(user__department=department_filter)
    
    if search:
        attendances = attendances.filter(
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(user__email__icontains=search)
        )
    
    # Get all departments for filter
    departments = User.objects.filter(role__in=['Employee', 'HR']).values_list('department', flat=True).distinct()
    
    context = {
        'attendances': attendances,
        'departments': departments,
        'date_filter': date_filter if date_filter else date.today().strftime('%Y-%m-%d'),
        'status_filter': status_filter,
        'department_filter': department_filter,
        'search': search,
    }
    
    return render(request, 'hr_module/attendance_list.html', context)

# Mark attendance
@login_required
def mark_attendance(request):
    if request.user.role != 'HR':
        messages.error(request, 'You do not have permission to mark attendance.')
        return redirect('login')
    
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.marked_by = request.user
            attendance.save()
            
            log_action(request.user, 'Mark Attendance', 
                      f"Marked attendance for {attendance.user.username} on {attendance.date} as {attendance.status}", 
                      request)
            
            messages.success(request, 'Attendance marked successfully.')
            return redirect('attendance_list')
    else:
        form = AttendanceForm()
    
    context = {'form': form}
    return render(request, 'hr_module/mark_attendance.html', context)

# Edit attendance
@login_required
def edit_attendance(request, attendance_id):
    if request.user.role != 'HR':
        messages.error(request, 'You do not have permission to edit attendance.')
        return redirect('login')
    
    attendance = get_object_or_404(Attendance, id=attendance_id)
    
    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            form.save()
            
            log_action(request.user, 'Edit Attendance', 
                      f"Edited attendance for {attendance.user.username} on {attendance.date}", 
                      request)
            
            messages.success(request, 'Attendance updated successfully.')
            return redirect('attendance_list')
    else:
        form = AttendanceForm(instance=attendance)
    
    context = {'form': form, 'attendance': attendance}
    return render(request, 'hr_module/edit_attendance.html', context)

# Bulk mark attendance
@login_required
def bulk_mark_attendance(request):
    if request.user.role != 'HR':
        messages.error(request, 'You do not have permission.')
        return redirect('login')
    
    if request.method == 'POST':
        attendance_date_str = request.POST.get('date')
        attendance_date = parse_date(attendance_date_str)
        department = request.POST.get('department', '')
        
        employees = User.objects.filter(role__in=['Employee', 'HR'], is_active=True)
        if department:
            employees = employees.filter(department=department)
        
        marked_count = 0
        for emp in employees:
            status = request.POST.get(f'status_{emp.id}')
            if status:
                Attendance.objects.update_or_create(
                    user=emp,
                    date=attendance_date,
                    defaults={
                        'status': status,
                        'marked_by': request.user
                    }
                )
                marked_count += 1
        
        log_action(request.user, 'Bulk Mark Attendance', 
                  f"Marked attendance for {marked_count} employees on {attendance_date}", 
                  request)
        
        messages.success(request, f'Attendance marked for {marked_count} employees.')
        return redirect('attendance_list')
    
    else:
        form = BulkAttendanceForm()
        attendance_date_str = request.GET.get('date', '')
        attendance_date = parse_date(attendance_date_str)
        department = request.GET.get('department', '')
        
        employees = User.objects.filter(role__in=['Employee', 'HR'], is_active=True)
        if department:
            employees = employees.filter(department=department)
        
        # Get existing attendance for the date
        existing_attendance = {}
        for att in Attendance.objects.filter(date=attendance_date, user__in=employees):
            existing_attendance[att.user.id] = att.status
        
        employees_data = []
        for emp in employees:
            employees_data.append({
                'employee': emp,
                'current_status': existing_attendance.get(emp.id, 'Absent')
            })
        
        departments = User.objects.filter(role__in=['Employee', 'HR']).values_list('department', flat=True).distinct()
        
        context = {
            'form': form,
            'employees_data': employees_data,
            'attendance_date': attendance_date,
            'department': department,
            'departments': departments,
        }
        return render(request, 'hr_module/bulk_mark_attendance.html', context)

# Leave requests list
@login_required
def leave_requests(request):
    if request.user.role != 'HR':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('login')
    
    # Filters
    status_filter = request.GET.get('status', 'Pending')
    search = request.GET.get('search', '')
    
    leaves = Leave.objects.select_related('user', 'approved_by').all()
    
    if status_filter:
        leaves = leaves.filter(status=status_filter)
    
    if search:
        leaves = leaves.filter(
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(user__email__icontains=search)
        )
    
    context = {
        'leaves': leaves,
        'status_filter': status_filter,
        'search': search,
    }
    
    return render(request, 'hr_module/leave_requests.html', context)

# Leave detail
@login_required
def leave_detail(request, leave_id):
    if request.user.role != 'HR':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('login')
    
    leave = get_object_or_404(Leave, id=leave_id)
    
    if request.method == 'POST':
        form = LeaveApprovalForm(request.POST, instance=leave)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.approved_by = request.user
            leave.save()
            
            # Mark attendance as on leave if approved
            if leave.status == 'Approved':
                current_date = leave.start_date
                while current_date <= leave.end_date:
                    Attendance.objects.update_or_create(
                        user=leave.user,
                        date=current_date,
                        defaults={
                            'status': 'On Leave',
                            'marked_by': request.user,
                            'notes': f'{leave.leave_type} - Approved'
                        }
                    )
                    current_date += timedelta(days=1)
            
            log_action(request.user, 'Leave Approval', 
                      f"{leave.status} leave request for {leave.user.username} from {leave.start_date} to {leave.end_date}", 
                      request)
            
            messages.success(request, f'Leave request {leave.status.lower()} successfully.')
            return redirect('leave_requests')
    else:
        form = LeaveApprovalForm(instance=leave)
    
    context = {
        'leave': leave,
        'form': form,
    }
    
    return render(request, 'hr_module/leave_detail.html', context)

# Apply leave (for employee)
@login_required
def apply_leave(request):
    if request.user.role != 'HR':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('login')
    
    if request.method == 'POST':
        form = LeaveForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.save()
            
            log_action(request.user, 'Apply Leave', 
                      f"Leave applied for {leave.user.username} from {leave.start_date} to {leave.end_date}", 
                      request)
            
            messages.success(request, 'Leave application submitted successfully.')
            return redirect('leave_requests')
    else:
        form = LeaveForm()
    
    context = {'form': form}
    return render(request, 'hr_module/apply_leave.html', context)

# Task list
@login_required
def task_list(request):
    if request.user.role != 'HR':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('login')
    
    # Filters
    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')
    search = request.GET.get('search', '')
    
    tasks = Task.objects.select_related('assigned_to', 'assigned_by').filter(assigned_by=request.user)
    
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)
    
    if search:
        tasks = tasks.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(assigned_to__first_name__icontains=search) |
            Q(assigned_to__last_name__icontains=search)
        )
    
    context = {
        'tasks': tasks,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
        'search': search,
    }
    
    return render(request, 'hr_module/task_list.html', context)

# Create task
@login_required
def create_task(request):
    if request.user.role != 'HR':
        messages.error(request, 'You do not have permission to create tasks.')
        return redirect('login')
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.assigned_by = request.user
            task.save()
            
            log_action(request.user, 'Create Task', 
                      f"Created task '{task.title}' for {task.assigned_to.username}", 
                      request)
            
            messages.success(request, 'Task created successfully.')
            return redirect('task_list')
    else:
        form = TaskForm()
    
    context = {'form': form}
    return render(request, 'hr_module/create_task.html', context)

# Task detail
@login_required
def task_detail(request, task_id):
    if request.user.role != 'HR':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('login')
    
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST':
        form = TaskStatusForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            if task.status == 'Completed':
                task.completed_at = timezone.now()
            task.save()
            
            log_action(request.user, 'Update Task', 
                      f"Updated task '{task.title}' status to {task.status}", 
                      request)
            
            messages.success(request, 'Task updated successfully.')
            return redirect('task_list')
    else:
        form = TaskStatusForm(instance=task)
    
    context = {
        'task': task,
        'form': form,
    }
    
    return render(request, 'hr_module/task_detail.html', context)

# Delete task
@login_required
def delete_task(request, task_id):
    if request.user.role != 'HR':
        messages.error(request, 'You do not have permission to delete tasks.')
        return redirect('login')
    
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST':
        task_title = task.title
        task.delete()
        
        log_action(request.user, 'Delete Task', 
                  f"Deleted task '{task_title}'", 
                  request)
        
        messages.success(request, 'Task deleted successfully.')
        return redirect('task_list')
    
    context = {'task': task}
    return render(request, 'hr_module/delete_task.html', context)

# Employee attendance report
@login_required
def employee_attendance_report(request, user_id):
    if request.user.role != 'HR':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('login')
    
    employee = get_object_or_404(User, id=user_id)
    
    # Date range filter
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    
    attendances = Attendance.objects.filter(user=employee)
    
    if start_date:
        attendances = attendances.filter(date__gte=start_date)
    if end_date:
        attendances = attendances.filter(date__lte=end_date)
    
    # Statistics
    total_days = attendances.count()
    present_days = attendances.filter(status='Present').count()
    absent_days = attendances.filter(status='Absent').count()
    leave_days = attendances.filter(status='On Leave').count()
    half_days = attendances.filter(status='Half Day').count()
    
    attendance_percentage = (present_days / total_days * 100) if total_days > 0 else 0
    
    context = {
        'employee': employee,
        'attendances': attendances,
        'total_days': total_days,
        'present_days': present_days,
        'absent_days': absent_days,
        'leave_days': leave_days,
        'half_days': half_days,
        'attendance_percentage': round(attendance_percentage, 2),
        'start_date': start_date,
        'end_date': end_date,
    }
    
    return render(request, 'hr_module/employee_attendance_report.html', context)

# Export attendance to CSV
@login_required
def export_attendance_csv(request):
    if request.user.role != 'HR':
        messages.error(request, 'You do not have permission.')
        return redirect('login')
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="attendance_report.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Employee Name', 'Email', 'Department', 'Date', 'Status', 'Check In', 'Check Out', 'Working Hours', 'Notes'])
    
    date_filter_str = request.GET.get('date', '')
    date_filter = parse_date(date_filter_str)
    attendances = Attendance.objects.filter(date=date_filter).select_related('user')
    
    for att in attendances:
        writer.writerow([
            f"{att.user.first_name} {att.user.last_name}",
            att.user.email,
            att.user.department or 'N/A',
            att.date,
            att.status,
            att.check_in_time or 'N/A',
            att.check_out_time or 'N/A',
            att.get_working_hours() or 'N/A',
            att.notes or ''
        ])
    
    log_action(request.user, 'Export Attendance', f"Exported attendance for {date_filter}", request)
    
    return response
