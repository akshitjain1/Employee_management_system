from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import random

# OTP model for password change
class OTP(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    attempts = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.otp_code:
            self.otp_code = str(random.randint(100000, 999999))
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=5)
        super().save(*args, **kwargs)
    
    def is_valid(self):
        return timezone.now() < self.expires_at and self.attempts < 3 and not self.is_verified
    
    def __str__(self):
        return f"OTP for {self.user.email}"

# track login attempts
class LoginAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    success = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.email} - {'Success' if self.success else 'Failed'}"

# audit log for admin actions
class AuditLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    details = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.action} by {self.user} at {self.timestamp}"

# notification log
class NotificationLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=50)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Sent')
    
    def __str__(self):
        return f"{self.notification_type} to {self.user.email}"
