from django.urls import path
from . import views
from . import profile_views

app_name = 'employee'

urlpatterns = [
    path('dashboard/', views.employee_dashboard, name='dashboard'),
    path('profile/', profile_views.employee_profile, name='employee_profile'),
    path('tasks/', views.employee_tasks, name='tasks'),
    path('tasks/<int:task_id>/update-status/', views.update_task_status, name='update_task_status'),
    path('tasks/<int:task_id>/accept/', views.accept_task, name='accept_task'),
    path('tasks/<int:task_id>/reject/', views.reject_task, name='reject_task'),
    path('attendance/', views.employee_attendance, name='attendance'),
    path('attendance/mark/', views.mark_attendance, name='mark_attendance'),
    path('leave/', views.employee_leave, name='leave'),
    path('leave/apply/', views.apply_leave, name='apply_leave'),
]