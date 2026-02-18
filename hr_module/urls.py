from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.hr_dashboard, name='hr_dashboard'),
    
    # Attendance URLs
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/mark/', views.mark_attendance, name='mark_attendance'),
    path('attendance/bulk/', views.bulk_mark_attendance, name='bulk_mark_attendance'),
    path('attendance/<int:attendance_id>/edit/', views.edit_attendance, name='edit_attendance'),
    path('attendance/report/<int:user_id>/', views.employee_attendance_report, name='employee_attendance_report'),
    path('attendance/export/', views.export_attendance_csv, name='export_attendance_csv'),
    
    # Leave
    path('leaves/', views.leave_requests, name='leave_requests'),
    path('leaves/<int:leave_id>/', views.leave_detail, name='leave_detail'),
    path('leaves/apply/', views.apply_leave, name='apply_leave'),
    
    # Tasks
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/delete/', views.delete_task, name='delete_task'),
]
