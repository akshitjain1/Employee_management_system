# Create your models here.
from django.conf import settings
from django.db import models

class EmployeeProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    date_of_joining = models.DateField(auto_now_add=True)
    is_employee = models.BooleanField(default=True)

    def __str__(self):
        return self.employee_id
    
class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Rejected', 'Rejected'),
    ]

    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.employee.email} - {self.date}"
    
# hr_module/models.py

class Task(models.Model):
    STATUS_CHOICES = [
        ('Assigned', 'Assigned'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('Completed', 'Completed'),
        ('Overdue', 'Overdue'),
    ]

    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    deadline = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Assigned')

    rejection_reason = models.TextField(blank=True, null=True)
    completion_file = models.FileField(upload_to='task_submissions/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

class Leave(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    document = models.FileField(upload_to='leave_documents/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    applied_on = models.DateTimeField(auto_now_add=True)
    
class Salary(models.Model):
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    month = models.CharField(max_length=20)  # e.g. "Jan 2026"
    basic = models.DecimalField(max_digits=10, decimal_places=2)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    payslip = models.FileField(upload_to='payslips/', blank=True, null=True)
    is_credited = models.BooleanField(default=False)
    credited_on = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.employee.username} - {self.month}"