"""
URL configuration for ems project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from admin_panel.views import user_login, user_logout, change_password_required, employee_dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_login, name='login'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('change-password/', change_password_required, name='change_password_required'),
    path('employee/dashboard/', employee_dashboard, name='employee_dashboard'),
    path('admin-panel/', include('admin_panel.urls')),
    path('hr/', include('hr_module.urls')),
]
