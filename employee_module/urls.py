from django.urls import path
from . import views
urlpatterns = [
    path('dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('tasks/', views.employee_tasks, name='employee_tasks'),
    path('tasks/<int:task_id>/accept/', views.accept_task, name='accept_task'),
    path('tasks/<int:task_id>/reject/', views.reject_task, name='reject_task'),
    path('tasks/<int:task_id>/complete/', views.complete_task, name='complete_task'),
    path('attendance/', views.employee_attendance, name='employee_attendance'),
    path('attendance/mark/', views.mark_attendance, name='mark_attendance'),
    path('leave/', views.employee_leave, name='employee_leave'),
     path('leave/apply/', views.apply_leave, name='apply_leave'),
    path('salary/', views.employee_salary, name='employee_salary'),
    path('register/', views.employee_register, name='employee_register'),
    path('login/', views.employee_login, name='employee_login'),
    path('logout/', views.employee_logout, name='employee_logout'),
]