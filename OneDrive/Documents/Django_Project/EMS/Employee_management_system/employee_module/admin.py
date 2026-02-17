from django.contrib import admin
from .models import EmployeeProfile, Attendance, Salary, Task, Leave
# Register your models here.
admin.site.register(EmployeeProfile)
admin.site.register(Attendance)
admin.site.register(Task)
admin.site.register(Leave)
admin.site.register(Salary)
