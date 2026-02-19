# This app uses models from hr_module and users app
# No separate models needed since CustomUser already has all employee fields
# and hr_module has Attendance, Leave, Task models

from django.db import models

# Employee module doesn't need separate models
# All functionality uses:
# - users.CustomUser for employee data
# - hr_module.Attendance for attendance
# - hr_module.Leave for leave management  
# - hr_module.Task for tasks