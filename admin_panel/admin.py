from django.contrib import admin
from .models import OTP, LoginAttempt, AuditLog, NotificationLog

admin.site.register(OTP)
admin.site.register(LoginAttempt)
admin.site.register(AuditLog)
admin.site.register(NotificationLog)
