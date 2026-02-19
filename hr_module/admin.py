from django.contrib import admin
from .models import Attendance, Leave, Task, LeaveBalance

# Register your models here.
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'status', 'check_in_time', 'check_out_time', 'marked_by']
    list_filter = ['status', 'date', 'user__department']
    search_fields = ['user__first_name', 'user__last_name', 'user__email']
    date_hierarchy = 'date'

@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ['user', 'leave_type', 'start_date', 'end_date', 'status', 'approved_by']
    list_filter = ['status', 'leave_type', 'start_date']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'reason']
    date_hierarchy = 'start_date'

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'assigned_to', 'assigned_by', 'priority', 'status', 'due_date']
    list_filter = ['priority', 'status', 'due_date']
    search_fields = ['title', 'description', 'assigned_to__first_name', 'assigned_to__last_name']
    date_hierarchy = 'due_date'

@admin.register(LeaveBalance)
class LeaveBalanceAdmin(admin.ModelAdmin):
    list_display = ['user', 'sick_leave', 'casual_leave', 'earned_leave', 'year']
    list_filter = ['year']
    search_fields = ['user__first_name', 'user__last_name', 'user__email']
