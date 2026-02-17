from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.views.decorators.http import require_POST
from employee_module.models import Task, Attendance, Leave, Salary
from .models import EmployeeProfile
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from functools import wraps

def employee_only(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('employee_login')
        if not hasattr(request.user, 'employeeprofile') or not request.user.employeeprofile.is_employee:
            messages.error(request, "Access denied. Employee account required.")
            return redirect('employee_login')
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required(login_url='employee_login')
@employee_only
def employee_dashboard(request):
    user = request.user
    today = now().date()

    # Employee Profile
    try:
        profile = EmployeeProfile.objects.get(user=user)
    except EmployeeProfile.DoesNotExist:
        messages.error(request, "Employee profile not found")
        return redirect('employee_login')

    # Attendance (today)
    attendance_today = Attendance.objects.filter(
        employee=user, date=today
    ).first()

    # Tasks
    total_tasks = Task.objects.filter(employee=user).count()
    active_tasks = Task.objects.filter(
        employee=user
    ).exclude(status='Completed').count()

    overdue_tasks = Task.objects.filter(
        employee=user, status='Overdue'
    ).count()

    # Leaves
    recent_leaves = Leave.objects.filter(
        employee=user
    ).order_by('-applied_on')[:3]

    leave_balance = 12 - Leave.objects.filter(
        employee=user, status='Approved'
    ).count()

    # Salary
    latest_salary = Salary.objects.filter(
        employee=user, is_credited=True
    ).order_by('-month').first()

    # Attendance graph data
    present_days = Attendance.objects.filter(
        employee=user, status='Present'
    ).count()

    absent_days = Attendance.objects.filter(
        employee=user, status='Absent'
    ).count()

    context = {
        'profile': profile,
        'attendance_today': attendance_today,
        'total_tasks': total_tasks,
        'active_tasks': active_tasks,
        'overdue_tasks': overdue_tasks,
        'recent_leaves': recent_leaves,
        'leave_balance': leave_balance,
        'salary': latest_salary,
        'present_days': present_days,
        'absent_days': absent_days,
    }

    return render(request, 'employee_dashboard/dashboard.html', context)

@login_required(login_url='employee_login')
@employee_only
def employee_tasks(request):
    tasks = Task.objects.filter(employee=request.user).order_by('-created_at')
    return render(request, 'employee_dashboard/tasks.html', {'tasks': tasks})

@login_required(login_url='employee_login')
@employee_only
@require_POST
def accept_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, employee=request.user)

    if task.status == "Assigned":
        task.status = "Accepted"
        task.save()
        messages.success(request, "Task accepted successfully")
    else:
        messages.warning(request, "Task cannot be accepted")

    return redirect('employee_tasks')

@login_required(login_url='employee_login')
@employee_only
@require_POST
def reject_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, employee=request.user)

    reason = request.POST.get('reason')

    if task.status == "Assigned" and reason:
        task.status = "Rejected"
        task.rejection_reason = reason
        task.save()
        messages.success(request, "Task rejected successfully")
    else:
        messages.warning(request, "Task cannot be rejected or reason not provided")

    return redirect('employee_tasks')

@login_required(login_url='employee_login')
@employee_only
@require_POST
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, employee=request.user)

    file = request.FILES.get('completion_file')

    if task.status == "Accepted" and file:
        task.status = "Completed"
        task.completion_file = file
        task.save()
        messages.success(request, "Task completed successfully")
    else:
        messages.warning(request, "Task cannot be completed or file not provided")

    return redirect('employee_tasks')

@login_required(login_url='employee_login')
@employee_only
def employee_attendance(request):
    attendance_records = Attendance.objects.filter(
        employee=request.user
    ).order_by('-date')

    return render(
        request,
        'employee_dashboard/attendance.html',
        {'attendance_records': attendance_records}
    )

@login_required(login_url='employee_login')
@employee_only
@require_POST
def mark_attendance(request):
    user = request.user
    today = now().date()
    
    # Check if attendance already marked today
    existing = Attendance.objects.filter(employee=user, date=today).first()
    if existing:
        messages.warning(request, "Attendance already marked for today")
        return redirect('employee_attendance')
    
    check_in = request.POST.get('check_in')
    check_out = request.POST.get('check_out')
    
    if not check_in or not check_out:
        messages.error(request, "Both check-in and check-out times are required")
        return redirect('employee_attendance')
    
    # Create attendance record
    Attendance.objects.create(
        employee=user,
        date=today,
        check_in=check_in,
        check_out=check_out,
        status='Pending'  # HR will approve/reject
    )
    
    messages.success(request, "Attendance marked successfully and sent for approval")
    return redirect('employee_attendance')

@login_required(login_url='employee_login')
@employee_only
def employee_leave(request):
    leaves = Leave.objects.filter(
        employee=request.user
    ).order_by('-applied_on')

    return render(
        request,
        'employee_dashboard/leave.html',
        {'leaves': leaves}
    )

@login_required(login_url='employee_login')
@employee_only
@require_POST
def apply_leave(request):
    user = request.user

    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    reason = request.POST.get('reason')
    document = request.FILES.get('document')  # optional

    # Basic validation
    if not (start_date and end_date and reason):
        messages.error(request, "All fields are required except document")
        return redirect('employee_leave')

    # Create leave request (HR will approve/reject)
    Leave.objects.create(
        employee=user,
        start_date=start_date,
        end_date=end_date,
        reason=reason,
        document=document,   # can be None
        status='Pending'
    )

    messages.success(request, "Leave application submitted successfully")
    return redirect('employee_leave')


@login_required(login_url='employee_login')
@employee_only
def employee_salary(request):
    """
    Employee can ONLY view salary details.
    HR controls creation, calculation, and crediting.
    """

    salaries = (
        Salary.objects
        .filter(employee=request.user)
        .order_by('-month')   # latest first
    )

    return render(
        request,
        'employee_dashboard/salary.html',
        {
            'salaries': salaries
        }
    )

def employee_login(request):
    # Redirect if already logged in
    if request.user.is_authenticated:
        if hasattr(request.user, 'employeeprofile') and request.user.employeeprofile.is_employee:
            return redirect('employee_dashboard')
    
    if request.method == "POST":
        emp_id = request.POST.get('employee_id')
        password = request.POST.get('password')

        if not emp_id or not password:
            messages.error(request, "Both fields are required")
            return render(request, 'employee_dashboard/login.html')

        try:
            employee = EmployeeProfile.objects.get(employee_id=emp_id)
            user = authenticate(request, username=employee.user.username, password=password)

            if user is not None and employee.is_employee:
                login(request, user)
                messages.success(request, f"Welcome {user.username}!")
                return redirect('employee_dashboard')
            else:
                messages.error(request, "Invalid credentials or not an employee account")

        except EmployeeProfile.DoesNotExist:
            messages.error(request, "Employee ID not found")

    return render(request, 'employee_dashboard/login.html')

def employee_register(request):
    # Redirect if already logged in
    if request.user.is_authenticated:
        return redirect('employee_dashboard')
    
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        employee_id = request.POST.get('employee_id')
        department = request.POST.get('department')
        designation = request.POST.get('designation')

        # Validation
        if not all([username, email, password, confirm_password, employee_id, department, designation]):
            messages.error(request, "All fields are required")
            return redirect('employee_register')

        # Password match check
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('employee_register')

        # Password strength check (optional)
        if len(password) < 6:
            messages.error(request, "Password must be at least 6 characters long")
            return redirect('employee_register')

        # Username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('employee_register')

        # Email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('employee_register')

        # Employee ID already exists
        if EmployeeProfile.objects.filter(employee_id=employee_id).exists():
            messages.error(request, "Employee ID already exists")
            return redirect('employee_register')

        try:
            # Create User
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            # Create Employee Profile
            EmployeeProfile.objects.create(
                user=user,
                employee_id=employee_id,
                department=department,
                designation=designation,
                is_employee=True  # Explicitly set to True
            )

            messages.success(request, "Employee registered successfully! Please login.")
            return redirect('employee_login')
        
        except Exception as e:
            messages.error(request, f"Registration failed: {str(e)}")
            return redirect('employee_register')

    return render(request, 'employee_dashboard/register.html')

@login_required(login_url='employee_login')
def employee_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully")
    return redirect('employee_login')