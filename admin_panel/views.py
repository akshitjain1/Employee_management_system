from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.http import HttpResponse, JsonResponse

from .models import OTP, LoginAttempt, AuditLog, NotificationLog
from .forms import EmployeeCreationForm, EmployeeEditForm, ChangePasswordForm
import json
import secrets
import string
import csv

User = get_user_model()

# get ip address
def get_client_ip(request):
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        ip = x_forwarded.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# make employee id
def make_employee_id(first_name, last_name, date_of_joining):
    year = date_of_joining.year if date_of_joining else timezone.now().year
    first = first_name.lower()
    
    if last_name:
        last = last_name.lower()
        base_id = f"{first}.{last}_{year}"
    else:
        base_id = f"{first}.ems_{year}"
    
    emp_id = base_id
    counter = 1
    while User.objects.filter(employee_id=emp_id).exists():
        if last_name:
            emp_id = f"{first}.{last}_{year}_{counter}"
        else:
            emp_id = f"{first}.ems_{year}_{counter}"
        counter += 1
    
    return emp_id

# make temp password
def make_temp_password(length=10):
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))

# make username
def make_username(first_name, last_name):
    if last_name:
        base = f"{first_name.lower()}.{last_name.lower()}"
    else:
        base = f"{first_name.lower()}.ems"
    
    username = base
    counter = 1
    while User.objects.filter(username=username).exists():
        username = f"{base}{counter}"
        counter += 1
    return username

def user_login(request):
    if request.user.is_authenticated:
        if request.user.must_change_password:
            return redirect('change_password_required')
        if request.user.role == 'Admin':
            return redirect('admin_dashboard')
        elif request.user.role == 'HR':
            return redirect('hr_dashboard')
        else:
            return redirect('employee_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
            
            if user.account_locked:
                messages.error(request, 'Your account is locked. Please contact admin.')
                return redirect('login')
            
            auth_user = authenticate(request, username=username, password=password)
            
            if auth_user:
                login(request, auth_user)
                user.failed_login_attempts = 0
                user.save()
                
                LoginAttempt.objects.create(
                    user=user,
                    email=user.email,
                    ip_address=get_client_ip(request),
                    success=True
                )
                
                AuditLog.objects.create(
                    user=user,
                    action='User Login',
                    details='Login successful',
                    ip_address=get_client_ip(request)
                )
                
                if user.must_change_password:
                    messages.info(request, 'You must change your temporary password.')
                    return redirect('change_password_required')
                
                if user.role == 'Admin':
                    return redirect('admin_dashboard')
                elif user.role == 'HR':
                    return redirect('hr_dashboard')
                else:
                    return redirect('employee_dashboard')
            else:
                user.failed_login_attempts += 1
                if user.failed_login_attempts >= 5:
                    user.account_locked = True
                    messages.error(request, 'Account locked due to too many failed attempts.')
                user.save()
                
                LoginAttempt.objects.create(
                    user=user,
                    email=user.email,
                    ip_address=get_client_ip(request),
                    success=False
                )
                
                messages.error(request, f'Invalid credentials. {5 - user.failed_login_attempts} attempts remaining.')
        
        except User.DoesNotExist:
            LoginAttempt.objects.create(
                email=username,
                ip_address=get_client_ip(request),
                success=False
            )
            messages.error(request, 'Invalid credentials.')
    
    return render(request, 'users/login.html')

@login_required
def change_password_required(request):
    if not request.user.must_change_password:
        if request.user.role == 'Admin':
            return redirect('admin_dashboard')
        elif request.user.role == 'HR':
            return redirect('hr_dashboard')
        else:
            return redirect('employee_dashboard')
    
    if request.method == 'POST':
        if 'send_otp' in request.POST:
            otp = OTP.objects.create(user=request.user)
            send_mail(
                'Your OTP Code for Password Change',
                f'Your OTP code is: {otp.otp_code}. Valid for 5 minutes.',
                settings.EMAIL_HOST_USER,
                [request.user.email],
                fail_silently=True,
            )
            NotificationLog.objects.create(
                user=request.user,
                notification_type='OTP',
                subject='OTP Code for Password Change',
                message=f'OTP sent: {otp.otp_code}'
            )
            messages.success(request, 'OTP sent to your email.')
            return render(request, 'users/change_password.html', {'otp_sent': True})
        
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            otp_code = form.cleaned_data['otp_code']
            new_password = form.cleaned_data['new_password']
            
            try:
                otp = OTP.objects.filter(user=request.user, is_verified=False).latest('created_at')
                
                if not otp.is_valid():
                    messages.error(request, 'OTP expired or maximum attempts reached.')
                    return redirect('change_password_required')
                
                otp.attempts += 1
                otp.save()
                
                if otp.otp_code == otp_code:
                    otp.is_verified = True
                    otp.save()
                    
                    request.user.set_password(new_password)
                    request.user.must_change_password = False
                    request.user.temp_password = None
                    request.user.save()
                    
                    AuditLog.objects.create(
                        user=request.user,
                        action='Password Changed',
                        details='Password changed',
                        ip_address=get_client_ip(request)
                    )
                    
                    messages.success(request, 'Password changed successfully! Please login with your new password.')
                    logout(request)
                    return redirect('login')
                else:
                    remaining = 3 - otp.attempts
                    messages.error(request, f'Invalid OTP. {remaining} attempts remaining.')
            
            except OTP.DoesNotExist:
                messages.error(request, 'No valid OTP found. Please request a new OTP.')
    
    return render(request, 'users/change_password.html')

def user_logout(request):
    if request.user.is_authenticated:
        AuditLog.objects.create(
            user=request.user,
            action='User Logout',
            details='Logout',
            ip_address=get_client_ip(request)
        )
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('login')

@login_required
def admin_dashboard(request):
    if request.user.role != 'Admin':
        messages.error(request, 'Unauthorized access.')
        return redirect('login')
    
    # getting counts
    total_emp = User.objects.filter(role='Employee').count()
    active_emp = User.objects.filter(role='Employee', is_active=True).count()
    total_hr = User.objects.filter(role='HR').count()
    total_sal = User.objects.filter(role='Employee').aggregate(Sum('salary'))['salary__sum'] or 0
    
    # chart data
    depts = list(User.objects.filter(role='Employee').values('department').annotate(count=Count('id')))
    dept_data = json.dumps(depts)
    
    recent_emp = User.objects.filter(role__in=['Employee', 'HR']).order_by('-date_joined')[:5]
    
    return render(request, 'admin_panel/dashboard.html', {
        'total_employees': total_emp,
        'active_employees': active_emp,
        'inactive_employees': total_emp - active_emp,
        'total_hr': total_hr,
        'total_salary': total_sal,
        'departments': dept_data,
        'recent_employees': recent_emp,
    })

@login_required
def create_employee(request):
    if request.user.role != 'Admin':
        messages.error(request, 'Unauthorized access.')
        return redirect('login')
    
    if request.method == 'POST':
        form = EmployeeCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            
            # make username
            username = make_username(user.first_name, user.last_name or '')
            user.username = username
            
            # make employee id
            user.employee_id = make_employee_id(user.first_name, user.last_name or '', user.date_of_joining)
            
            # temp password for first time
            temp_pass = make_temp_password()
            user.set_password(temp_pass)
            user.temp_password = temp_pass
            user.must_change_password = True
            
            user.save()
            
            AuditLog.objects.create(
                user=request.user,
                action='Employee Created',
                details=f'Created employee {user.username}',
                ip_address=get_client_ip(request)
            )
            
            email_body = f"""Welcome to EMS!

Your account has been created successfully.

Login Credentials:
Employee ID: {user.employee_id}
Username: {username}
Temporary Password: {temp_pass}

Please login at: http://127.0.0.1:8000/

IMPORTANT: You will be required to change your password on first login.
An OTP will be sent to this email for password verification.

Name: {user.get_full_name()}
Email: {user.email}
Department: {user.department}
Role: {user.role}

Best regards,
EMS Admin Team"""
            
            send_mail(
                'Welcome to EMS - Your Login Credentials',
                email_body,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            
            NotificationLog.objects.create(
                user=user,
                notification_type='Account Creation',
                subject='Welcome to EMS - Login Credentials',
                message=f'Temporary credentials sent. Username: {username}'
            )
            
            messages.success(request, f'Employee created! Username: {username} | Temporary password sent to {user.email}')
            return redirect('employee_list')
    else:
        form = EmployeeCreationForm()
    
    return render(request, 'admin_panel/create_employee.html', {'form': form})

@login_required
def employee_list(request):
    if request.user.role != 'Admin':
        messages.error(request, 'Unauthorized access.')
        return redirect('login')
    
    emps = User.objects.filter(role__in=['Employee', 'HR'])
    
    # search part
    search = request.GET.get('search', '')
    if search:
        emps = emps.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search) |
            Q(employee_id__icontains=search)
        )
    
    # filter by role
    role_filter = request.GET.get('role', '')
    if role_filter:
        emps = emps.filter(role=role_filter)
    
    # filter by department
    dept_filter = request.GET.get('department', '')
    if dept_filter:
        emps = emps.filter(department=dept_filter)
    
    # filter by status
    status = request.GET.get('status', '')
    if status == 'active':
        emps = emps.filter(is_active=True, account_locked=False)
    elif status == 'inactive':
        emps = emps.filter(is_active=False)
    elif status == 'locked':
        emps = emps.filter(account_locked=True)
    
    # get departments
    depts = User.objects.filter(role__in=['Employee', 'HR']).values_list('department', flat=True).distinct()
    depts = [d for d in depts if d]
    
    emps = emps.order_by('-date_joined')
    
    return render(request, 'admin_panel/employee_list.html', {
        'employees': emps,
        'departments': depts,
        'search_query': search,
        'role_filter': role_filter,
        'department_filter': dept_filter,
        'status_filter': status,
    })

@login_required
def employee_detail(request, user_id):
    if request.user.role != 'Admin':
        messages.error(request, 'Unauthorized access.')
        return redirect('login')
    
    emp = get_object_or_404(User, id=user_id)
    
    return render(request, 'admin_panel/employee_detail.html', {'employee': emp})

@login_required
def edit_employee(request, user_id):
    if request.user.role != 'Admin':
        messages.error(request, 'Unauthorized access.')
        return redirect('login')
    
    emp = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = EmployeeEditForm(request.POST, instance=emp)
        if form.is_valid():
            form.save()
            
            AuditLog.objects.create(
                user=request.user,
                action='Employee Updated',
                details=f'Updated {emp.email}',
                ip_address=get_client_ip(request)
            )
            
            messages.success(request, 'Employee updated successfully!')
            return redirect('employee_detail', user_id=emp.id)
    else:
        form = EmployeeEditForm(instance=emp)
    
    return render(request, 'admin_panel/edit_employee.html', {'form': form, 'employee': emp})

@login_required
def toggle_employee_status(request, user_id):
    if request.user.role != 'Admin':
        messages.error(request, 'Unauthorized access.')
        return redirect('login')
    
    emp = get_object_or_404(User, id=user_id)
    emp.is_active = not emp.is_active
    emp.save()
    
    status = 'activated' if emp.is_active else 'deactivated'
    
    AuditLog.objects.create(
        user=request.user,
        action=f'Employee {status}',
        details=f'{status} {emp.email}',
        ip_address=get_client_ip(request)
    )
    
    messages.success(request, f'Employee {status} successfully!')
    return redirect('employee_list')

@login_required
def unlock_account(request, user_id):
    if request.user.role != 'Admin':
        messages.error(request, 'Unauthorized access.')
        return redirect('login')
    
    emp = get_object_or_404(User, id=user_id)
    emp.account_locked = False
    emp.failed_login_attempts = 0
    emp.save()
    
    AuditLog.objects.create(
        user=request.user,
        action='Account Unlocked',
        details=f'Unlocked {emp.email}',
        ip_address=get_client_ip(request)
    )
    
    messages.success(request, 'Account unlocked successfully!')
    return redirect('employee_detail', user_id=emp.id)

@login_required
def delete_employee(request, user_id):
    if request.user.role != 'Admin':
        messages.error(request, 'Unauthorized access.')
        return redirect('login')
    
    emp = get_object_or_404(User, id=user_id)
    
    if emp.role == 'Admin':
        messages.error(request, 'Cannot delete admin users!')
        return redirect('employee_list')
    
    if request.method == 'POST':
        emp_email = emp.email
        emp_name = emp.get_full_name()
        
        AuditLog.objects.create(
            user=request.user,
            action='Employee Deleted',
            details=f'Deleted {emp_name}',
            ip_address=get_client_ip(request)
        )
        
        emp.delete()
        messages.success(request, f'Employee {emp_name} deleted successfully!')
        return redirect('employee_list')
    
    return render(request, 'admin_panel/delete_employee.html', {'employee': emp})

@login_required
def reset_employee_password(request, user_id):
    if request.user.role != 'Admin':
        messages.error(request, 'Unauthorized access.')
        return redirect('login')
    
    emp = get_object_or_404(User, id=user_id)
    
    # make new temp password
    temp_pass = make_temp_password()
    emp.set_password(temp_pass)
    emp.temp_password = temp_pass
    emp.must_change_password = True
    emp.save()
    
    # send email
    email_body = f"""Hello {emp.get_full_name()},

Your password has been reset by the administrator.

Your new temporary credentials:
Username: {emp.username}
Temporary Password: {temp_pass}

Login at: http://127.0.0.1:8000/

You will be required to change this password on first login.

Best regards,
EMS Admin Team"""
    
    send_mail(
        'EMS - Password Reset',
        email_body,
        settings.EMAIL_HOST_USER,
        [emp.email],
        fail_silently=False,
    )
    
    NotificationLog.objects.create(
        user=emp,
        notification_type='Password Reset',
        subject='Password Reset by Admin',
        message='Temporary password sent via email'
    )
    
    AuditLog.objects.create(
        user=request.user,
        action='Password Reset',
        details=f'Reset password for {emp.email}',
        ip_address=get_client_ip(request)
    )
    
    messages.success(request, f'Password reset! Temporary password sent to {emp.email}')
    return redirect('employee_detail', user_id=emp.id)

@login_required
def bulk_action(request):
    # bulk operations on selected employees
    if request.user.role != 'Admin':
        return JsonResponse({'success': False, 'message': 'Unauthorized'})
    
    if request.method == 'POST':
        action = request.POST.get('action')
        ids = request.POST.getlist('employee_ids[]')
        
        if not ids:
            return JsonResponse({'success': False, 'message': 'No employees selected'})
        
        emps = User.objects.filter(id__in=ids, role__in=['Employee', 'HR'])
        count = emps.count()
        
        if action == 'activate':
            emps.update(is_active=True)
            AuditLog.objects.create(
                user=request.user,
                action='Bulk Activate',
                details=f'Activated {count} employees',
                ip_address=get_client_ip(request)
            )
            return JsonResponse({'success': True, 'message': f'{count} employees activated'})
        
        elif action == 'deactivate':
            emps.update(is_active=False)
            AuditLog.objects.create(
                user=request.user,
                action='Bulk Deactivate',
                details=f'Deactivated {count} employees',
                ip_address=get_client_ip(request)
            )
            return JsonResponse({'success': True, 'message': f'{count} employees deactivated'})
        
        elif action == 'delete':
            emp_names = ', '.join([e.get_full_name() for e in emps])
            emps.delete()
            AuditLog.objects.create(
                user=request.user,
                action='Bulk Delete',
                details=f'Deleted {count} employees',
                ip_address=get_client_ip(request)
            )
            return JsonResponse({'success': True, 'message': f'{count} employees deleted'})
        
        elif action == 'unlock':
            emps.update(account_locked=False, failed_login_attempts=0)
            AuditLog.objects.create(
                user=request.user,
                action='Bulk Unlock',
                details=f'Unlocked {count} accounts',
                ip_address=get_client_ip(request)
            )
            return JsonResponse({'success': True, 'message': f'{count} accounts unlocked'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@login_required
def export_employees_csv(request):
    if request.user.role != 'Admin':
        messages.error(request, 'Unauthorized access.')
        return redirect('login')
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="employees_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Employee ID', 'First Name', 'Last Name', 'Email', 'Phone', 'Role', 
                     'Department', 'Salary', 'Date of Joining', 'Status', 'Account Locked'])
    
    emps = User.objects.filter(role__in=['Employee', 'HR']).order_by('employee_id')
    
    for emp in emps:
        writer.writerow([
            emp.employee_id or 'N/A',
            emp.first_name,
            emp.last_name,
            emp.email,
            emp.phone or 'N/A',
            emp.role,
            emp.department or 'N/A',
            emp.salary or 0,
            emp.date_of_joining.strftime('%Y-%m-%d') if emp.date_of_joining else 'N/A',
            'Active' if emp.is_active else 'Inactive',
            'Yes' if emp.account_locked else 'No'
        ])
    
    AuditLog.objects.create(
        user=request.user,
        action='Export Employees',
        details=f'Exported {emps.count()} employees',
        ip_address=get_client_ip(request)
    )
    
    return response

@login_required
def send_notification(request, user_id):
    if request.user.role != 'Admin':
        messages.error(request, 'Unauthorized access.')
        return redirect('login')
    
    emp = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        if subject and message:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [emp.email],
                fail_silently=False,
            )
            
            NotificationLog.objects.create(
                user=emp,
                notification_type='Admin Notice',
                subject=subject,
                message=message
            )
            
            AuditLog.objects.create(
                user=request.user,
                action='Send Notification',
                details=f'Sent to {emp.email}',
                ip_address=get_client_ip(request)
            )
            
            messages.success(request, 'Notification sent successfully!')
            return redirect('employee_detail', user_id=emp.id)
        else:
            messages.error(request, 'Subject and message are required!')
    
    return render(request, 'admin_panel/send_notification.html', {'employee': emp})

@login_required
def employee_login_history(request, user_id):
    if request.user.role != 'Admin':
        messages.error(request, 'Unauthorized access.')
        return redirect('login')
    
    emp = get_object_or_404(User, id=user_id)
    login_hist = LoginAttempt.objects.filter(user=emp).order_by('-timestamp')[:50]
    
    return render(request, 'admin_panel/employee_login_history.html', {
        'employee': emp,
        'login_attempts': login_hist
    })

@login_required
def audit_logs(request):
    if request.user.role != 'Admin':
        messages.error(request, 'Unauthorized access.')
        return redirect('login')
    
    logs = AuditLog.objects.all().order_by('-timestamp')[:100]
    
    return render(request, 'admin_panel/audit_logs.html', {'logs': logs})

def hr_dashboard(request):
    return render(request, 'hr_module/dashboard.html')

def employee_dashboard(request):
    return render(request, 'employee_module/dashboard.html')
