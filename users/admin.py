from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'role', 'employee_id', 'is_active', 'must_change_password', 'account_locked']
    list_filter = ['role', 'is_active', 'must_change_password', 'account_locked']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone', 'employee_id', 'department', 'salary', 'date_of_joining')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Security', {'fields': ('must_change_password', 'temp_password', 'account_locked', 'failed_login_attempts')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'is_active')}
        ),
    )
    search_fields = ('email', 'employee_id')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
