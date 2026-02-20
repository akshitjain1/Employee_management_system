from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['profile_pic_preview', 'email', 'get_display_name', 'role', 'employee_id', 'is_active', 'must_change_password', 'account_locked']
    list_filter = ['role', 'is_active', 'must_change_password', 'account_locked']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'nickname', 'phone', 'date_of_birth', 'bio', 'address')}),
        ('Profile', {'fields': ('profile_picture', 'profile_pic_preview')}),
        ('Employment Info', {'fields': ('employee_id', 'department', 'salary', 'date_of_joining')}),
        ('Emergency Contact', {'fields': ('emergency_contact_name', 'emergency_contact_phone')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Security', {'fields': ('must_change_password', 'temp_password', 'account_locked', 'failed_login_attempts')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'is_active')}
        ),
    )
    readonly_fields = ['profile_pic_preview']
    search_fields = ('email', 'employee_id', 'first_name', 'last_name', 'nickname')
    ordering = ('email',)
    
    def profile_pic_preview(self, obj):
        """Display profile picture thumbnail in admin"""
        if obj.profile_picture:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%; object-fit: cover;" />', obj.profile_picture.url)
        return format_html('<i class="fas fa-user-circle" style="font-size: 50px; color: #ccc;"></i>')
    profile_pic_preview.short_description = 'Photo'
    
    def get_display_name(self, obj):
        """Display full name or nickname"""
        full_name = obj.get_full_name()
        if obj.nickname:
            return f"{full_name} ({obj.nickname})"
        return full_name if full_name else obj.username
    get_display_name.short_description = 'Name'

admin.site.register(CustomUser, CustomUserAdmin)
