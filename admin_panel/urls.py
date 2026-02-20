from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('profile/', views.admin_profile, name='admin_profile'),
    path('create-employee/', views.create_employee, name='create_employee'),
    path('employees/', views.employee_list, name='employee_list'),
    path('employee/<int:user_id>/', views.employee_detail, name='employee_detail'),
    path('employee/<int:user_id>/edit/', views.edit_employee, name='edit_employee'),
    path('employee/<int:user_id>/delete/', views.delete_employee, name='delete_employee'),
    path('employee/<int:user_id>/toggle-status/', views.toggle_employee_status, name='toggle_employee_status'),
    path('employee/<int:user_id>/unlock/', views.unlock_account, name='unlock_account'),
    path('employee/<int:user_id>/reset-password/', views.reset_employee_password, name='reset_employee_password'),
    path('employee/<int:user_id>/send-notification/', views.send_notification, name='send_notification'),
    path('employee/<int:user_id>/login-history/', views.employee_login_history, name='employee_login_history'),
    path('employees/bulk-action/', views.bulk_action, name='bulk_action'),
    path('employees/export-csv/', views.export_employees_csv, name='export_employees_csv'),
    path('audit-logs/', views.audit_logs, name='audit_logs'),
]
