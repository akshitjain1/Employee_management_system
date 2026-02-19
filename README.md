
# Employee Management System (EMS)

Django-based Employee Management System for managing employees, HR staff, and admin operations.

## Project Team
This project was developed collaboratively by college students:
- Admin Panel & Authentication - Team Member 1
- HR Module & Reporting - Team Member 2  
- Employee Portal - Team Member 3

## Features

### Admin Panel
- Dashboard with statistics and charts 
- Employee Management - create, view, edit, delete employees
- Search and filter employees by role, department, status
- Bulk actions (activate/deactivate multiple employees at once)
- Export employee data to CSV
- Auto-generated Employee IDs (EMP-YYYY-XXXX format)
- Audit logs to track admin actions
- Account locking/unlocking and password reset

### HR Module
- Dashboard with statistics (attendance, leave, tasks)
- Attendance Management - mark individual/bulk attendance, view attendance records
- Leave Management - approve/reject leave requests, view leave history
- Task Management - assign tasks to employees, track progress and deadlines
- Employee attendance reports with filtering
- Export attendance data to CSV
- Real-time statistics and charts

### Employee Module ✅ (Recently Added)
- Personal dashboard with task, leave, and attendance statistics
- **Task Management:**
  - Accept or reject assigned tasks with reason
  - View and update task status (Pending → In Progress → Completed)
  - Submit files when completing tasks (mandatory)
  - View task submission files and rejection reasons
- **Attendance Management:**
  - Self-mark attendance with check-in/check-out times
  - HR verification system (pending/verified status)
  - View attendance records and statistics
  - Calculate attendance percentage
- **Leave Management:**
  - Apply for leaves with overlap detection
  - View leave balance by type (Sick, Casual, Earned)
  - Track leave application status
- Modern responsive UI with Tailwind CSS

### Authentication 
- Username and password login
- New employees get temporary passwords via email
- OTP verification when changing passwords (6-digit code, expires in 5 minutes)
- Account locks after 5 failed login attempts
- Email notifications for important events
- Role-based redirections: Admin → Admin Panel, HR → HR Dashboard, Employee → Employee Portal

## Requirements

- Python 3.10+
- pip
- Gmail account for sending emails

## Setup Instructions

### 1. Navigate to project folder
```bash
cd "Django Final Project/EMS/ems"
```

### 2. Create and activate virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install packages
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
# Copy the example file
cp .env.example .env

# Edit .env with your details
# Important: Add your Gmail credentials for email functionality
```

**Gmail Setup** (needed for sending emails):
1. Go to https://myaccount.google.com/security
2. Enable 2-Step Verification
3. Create App Password at https://myaccount.google.com/apppasswords
4. Copy the 16-digit password to .env file

### 5. Setup database
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create admin account
```bash
python manage.py createsuperuser --username admin --email admin@ems.com
# Password: admin (or whatever you want)
```

### 7. Start the server
```bash
python manage.py runserver
```

### 8. Login
- Open browser: http://127.0.0.1:8000/
- Username: write your username
- Password: write your password (or what you set)

## How to Use

### Creating Employees
1. Login as admin
2. Click "Create Employee" button
3. Fill in the employee details
4. System automatically generates username and temporary password
5. Employee gets an email with their login credentials
6. When they first login, they have to change their password using OTP

### Managing Employees
- View all employees with search and filters
- Edit employee information
- Activate or deactivate accounts
- Delete employees (asks for confirmation)
- Unlock locked accounts
- Reset passwords (generates new temp password)
- Send custom emails to employees
- See login history
- Bulk actions on multiple employees
- Export all data to CSV

### Admin Dashboard
Shows statistics like:
- Total employees
- Active/inactive counts
- Total HR staff
- Salary expenditure
- Department wise distribution (chart)
- Recent employees list

### HR Dashboard
Shows statistics like:
- Total employees and attendance today (present/absent/on leave)
- Pending leave requests
- Task statistics (pending, overdue)
- Department wise employee distribution (chart)
- Recent leave requests and tasks

## Tech Stack

- Django 5.1.7
- SQLite (database)
- Bootstrap 5 (for UI)
- Chart.js (for charts)
- Gmail SMTP (for emails)

## Security Features

- Passwords are hashed (Django built-in)
- CSRF protection enabled
- Login attempts tracked with IP address
- Account locks after 5 failed login attempts
- OTP verification for password changes
- Audit logs for admin actions
- Role-based access (Admin, HR, Employee)
- Sensitive data in .env file (not in git)

## Important Security Notes

**Don't push these to GitHub:**
- .env file (has email passwords)
- db.sqlite3 (has user data)
- *.log files

**Before deploying to production:**
- Set DEBUG=False
- Change SECRET_KEY
- Use PostgreSQL instead of SQLite
- Setup HTTPS  

## Project Structure

```
ems/
├── admin_panel/          # Admin features (completed)
├── hr_module/            # HR features (completed)
├── employee_module/      # Employee features (not implemented)
├── users/                # User model and authentication
├── templates/            # HTML files
├── static/               # CSS, JS files
└── ems/                  # Django settings
```

## User Roles

**Admin**
- Can do everything
- Create/edit/delete employees and HR
- View all data and reports
- Manage accounts and permissions

**HR**
- Manage attendance (mark individual/bulk, view records)
- Approve/reject leave requests
- Assign and track tasks
- View employee attendance reports
- Export attendance data
- Dashboard with real-time statistics

**Employee** (coming soon)
- View personal info
- Apply for leave
- Mark attendance

## Development Status

| Feature | Status |
|---------|--------|
| User authentication | Done |
| Admin dashboard | Done |
| Employee CRUD | Done |
| Search & filters | Done |
| Bulk actions | Done |
| CSV export | Done |
| Email system | Done |
| Login tracking | Done |
| Audit logs | Done |
| OTP verification | Done |
| Attendance Management | Done |
| Leave Management | Done |
| Task Management | Done |
| HR Dashboard | Done |
| Employee Module | Not started |

## Testing

```bash
# Check for errors
python manage.py check

# Run tests
python manage.py test

# Check migrations
python manage.py showmigrations
```

## Environment Variables

Create a .env file with these variables:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=EMS <your-email@gmail.com>
```

## Notes

- This is a college project for learning Django
- Admin panel is fully functional
- HR module is fully functional with attendance, leave, and task management
- Employee module is planned but not implemented yet
- Email functionality requires Gmail account with app password

---

**Created for**: Django Final Project  
**Author**: Student Project
