# Employee Management System (EMS)

Modern Django-based Employee Management System with a professional public website for managing employees, HR staff, and admin operations.

## 🎯 Project Overview
This comprehensive EMS was developed collaboratively by college students as a final Django project, featuring a complete employee lifecycle management system with modern UI/UX design.

## ✨ Key Features

### 🏠 Public Website (UPDATED - Professional Design)
- **Modern Landing Page** with animated hero carousel and parallax effects
- **Fixed Header** with top contact bar and professional navigation
- **Service Pages** (6 pages):
  - Application Development
  - Web Development
  - CMS & E-Commerce
  - Digital Marketing
  - Website Designing
  - Mobile Applications
- **About Page** with minimalist design, company stats, mission & vision
- **Contact Page** with interactive form and info cards
- **Quote Request Page** for project inquiries
- **Professional Footer** with quick links, services, and contact info
- **WhatsApp Integration** with floating button
- **Responsive Design** that works perfectly on all devices
- **Smooth Animations** and scroll effects throughout
- **Modern Color Scheme** with gradient text effects
- **Plus Jakarta Sans** professional typography

### 👨‍💼 Admin Panel
- Dashboard with statistics and interactive charts 
- Employee Management - create, view, edit, delete employees
- Search and filter employees by role, department, status
- Bulk actions (activate/deactivate multiple employees at once)
- Export employee data to CSV
- Auto-generated Employee IDs (EMP-YYYY-XXXX format)
- Audit logs to track all admin actions
- Account locking/unlocking and password reset
- Employee login history tracking

### 👥 HR Module
- Dashboard with real-time statistics (attendance, leave, tasks)
- **Attendance Management:** 
  - Mark individual/bulk attendance
  - Verify employee self-marked attendance
  - View attendance records with filtering
  - Generate attendance reports
- **Leave Management:** 
  - Approve/reject leave requests
  - View leave history and balance
  - Track leave types (Sick, Casual, Earned, etc.)
- **Task Management:** 
  - Assign tasks to employees with file attachments (NEW)
  - Track task progress and deadlines
  - View task submissions from employees
  - Set priority levels (Low, Medium, High, Urgent)
- Export attendance data to CSV
- Real-time statistics and charts

### 💼 Employee Module
- Personal dashboard with task, leave, and attendance statistics
- **Task Management:**
  - Accept or reject assigned tasks with reason
  - View HR-uploaded task attachment files (NEW)
  - Update task status (Pending → In Progress → Completed)
  - Submit files when completing tasks (mandatory)
  - View task history and rejection reasons
- **Attendance Management:**
  - Self-mark attendance with check-in/check-out times
  - View attendance records and statistics
  - Track attendance percentage
- **Leave Management:**
  - Apply for leaves with overlap detection
  - View leave balance by type
  - Track leave application status
- Modern responsive UI with smooth animations

### 🔐 Authentication & Security
- Username and password login
- New employees receive temporary passwords via email
- OTP verification for password changes (6-digit code, 5-minute expiry)
- Account locks after 5 failed login attempts
- Email notifications for important events
- Role-based redirections (Admin/HR/Employee)
- Audit trail for all admin actions

## 📋 Requirements

- Python 3.10+
- pip (Python package manager)
- Gmail account for sending emails (or any SMTP server)

## 🚀 Setup Instructions

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd ems
```

### 2. Create and activate virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
# Copy the example file
cp .env.example .env

# Edit .env with your details
```

**Required Environment Variables:**
- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to True for development, False for production
- `EMAIL_HOST_USER`: Your Gmail address
- `EMAIL_HOST_PASSWORD`: Gmail app password (see below)

**Gmail Setup for Email:**
1. Go to https://myaccount.google.com/security
2. Enable 2-Step Verification
3. Generate App Password at https://myaccount.google.com/apppasswords
4. Copy the 16-digit password to your .env file

### 5. Setup database
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create superuser (Admin)
```bash
python manage.py createsuperuser
```

### 7. Add logo and background images (Optional)
Place your images in the `static/images/` directory:
- `logo.png` - Company logo for navigation
- `background.png` - Hero section background (optional, gradient fallback included)

### 8. Start the development server
```bash
python manage.py runserver
```

### 9. Access the application
- **Home Page**: http://127.0.0.1:8000/
- **Login**: http://127.0.0.1:8000/login/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## 📚 User Guide

### For Admins

**Creating Employees:**
1. Login with admin credentials
2. Navigate to Admin Dashboard
3. Click "Create Employee"
4. Fill in employee details
5. System auto-generates username and temporary password
6. Employee receives email with login credentials

**Managing Employees:**
- View all employees with search/filter options
- Edit employee information
- Activate/deactivate accounts
- Delete employees with confirmation
- Unlock locked accounts
- Reset passwords
- Send notifications
- Export data to CSV
- Perform bulk actions

### For HR Staff

**Managing Attendance:**
- Mark individual or bulk attendance
- Verify employee self-marked attendance
- View attendance records with filters
- Generate attendance reports
- Export to CSV

**Managing Leaves:**
- Review pending leave requests
- Approve or reject with remarks
- View leave history
- Track leave balances

**Managing Tasks:**
- Create tasks and assign to employees
- Upload reference documents/files
- Set priority and due dates
- Track task progress
- View employee submissions
- Update task status

### For Employees

**Task Workflow:**
1. Accept or reject assigned tasks
2. Download task attachment files (if provided)
3. Start working (status: In Progress)
4. Upload submission file when complete
5. Submit for review

**Attendance:**
- Self-mark daily attendance
- View attendance history
- Track attendance percentage

**Leave Application:**
- Apply for leave with dates and reason
- Check leave balance
- Track application status

## 🛠️ Tech Stack

- **Backend**: Django 5.2.11
- **Database**: SQLite (development), PostgreSQL recommended for production
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **UI Framework**: Bootstrap 5
- **Charts**: Chart.js
- **Email**: SMTP (Gmail)
- **Authentication**: Django built-in with custom OTP

## 🔒 Security Features

✅ Password hashing with Django's built-in system
✅ CSRF protection enabled
✅ Login attempt tracking with IP logging
✅ Account lockout after failed attempts
✅ OTP verification for password changes
✅ Role-based access control (RBAC)
✅ Audit logs for admin actions
✅ Environment variables for sensitive data
✅ SQL injection protection (Django ORM)

## ⚠️ Important Security Notes

**Never commit these files to GitHub:**
- `.env` - Contains sensitive credentials
- `db.sqlite3` - Contains user data
- `*.log` - May contain sensitive information
- `media/` - User-uploaded files

**Before deploying to production:**
- Set `DEBUG=False` in .env
- Change `SECRET_KEY` to a new random value
- Use PostgreSQL instead of SQLite
- Setup HTTPS/SSL
- Configure proper ALLOWED_HOSTS
- Use environment-specific settings
- Enable security middleware
- Setup proper backup system

## 📁 Project Structure

```
ems/
├── admin_panel/          # Admin features & employee management
├── hr_module/            # HR dashboard & operations
├── employee_module/      # Employee portal & self-service
├── home/                 # Public website (NEW)
├── users/                # Custom user model & authentication
├── templates/            # HTML templates
│   ├── admin_panel/
│   ├── hr_module/
│   ├── employee_module/
│   ├── home/            # Public website templates (NEW)
│   └── users/
├── static/              # CSS, JS, images
│   ├── images/          # Logo and backgrounds
│   └── styles.css
├── media/               # User uploads (gitignored)
│   ├── task_attachments/    # HR uploaded files (NEW)
│   └── task_submissions/    # Employee submissions
├── ems/                 # Django project settings
├── manage.py
├── requirements.txt
├── .env.example
└── .gitignore
```

## 👥 User Roles & Permissions

| Feature | Admin | HR | Employee |
|---------|-------|-----|----------|
| Manage employees | ✅ | ❌ | ❌ |
| View all attendance | ✅ | ✅ | Own only |
| Mark attendance | ✅ | ✅ | ✅ |
| Verify attendance | ✅ | ✅ | ❌ |
| Manage leaves | ✅ | ✅ | Apply only |
| Assign tasks | ✅ | ✅ | ❌ |
| Upload task files | ✅ | ✅ | Submissions only |
| View audit logs | ✅ | ❌ | ❌ |
| Export data | ✅ | ✅ | ❌ |

## 📊 Development Status

| Module | Status | Features |
|--------|--------|----------|
| Public Website | ✅ Complete | Landing, About, Contact pages |
| Authentication | ✅ Complete | Login, OTP, Password reset |
| Admin Panel | ✅ Complete | Full CRUD, Audit logs |
| HR Module | ✅ Complete | Attendance, Leave, Tasks with files |
| Employee Module | ✅ Complete | Dashboard, Tasks, Attendance, Leave |
| Email System | ✅ Complete | Notifications, OTP |
| File Upload | ✅ Complete | Task attachments & submissions |

## 🧪 Testing

```bash
# Check for errors
python manage.py check

# Run tests
python manage.py test

# Check migrations
python manage.py showmigrations

# Validate templates
python manage.py validate_templates
```

## 🌐 Environment Variables

Create a `.env` file in the project root:

```env
# Django Settings
SECRET_KEY=your-django-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite for development)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# Email Configuration (Gmail)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-digit-app-password
DEFAULT_FROM_EMAIL=EMS <your-email@gmail.com>
```

## 📝 Contributing

This is a student project, but suggestions and improvements are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is created for educational purposes as part of a college final project.

## 🙏 Acknowledgments

- Django Documentation
- Bootstrap Team
- Chart.js Team
- All open-source contributors

---

**Project Type**: College Final Project  
**Framework**: Django  
**Year**: 2026

For questions or issues, please open an issue on GitHub.

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
