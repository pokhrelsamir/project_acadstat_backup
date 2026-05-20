# AcadStat - Academic Statistics System

## Project Structure

```
djangoacadstat/
├── academicsys/
│   ├── __init__.py
│   ├── settings.py          # Django settings, AI config, email config
│   ├── urls.py
│   └── wsgi.py
├── core/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   ├── migrations/
│   │   ├── __init__.py
│   │   ├── 0001_initial.py
│   │   ├── 0002_student_image.py
│   │   └── 0003_student_semester.py
│   └── management/commands/
│       ├── __init__.py
│       ├── create_student_user.py
│       ├── create_all_student_users.py
│       ├── list_students.py
│       └── send_notifications.py  # Automation command
├── templates/core/
│   ├── dashboard/
│   │   ├── home.html
│   │   ├── dashboard.html
│   │   ├── marks_list.html
│   │   ├── student_analysis.html
│   │   └── ...
│   └── registration/
│       └── login.html
├── media/
│   └── student_images/
├── static/
│   └── css/style.css
├── manage.py
├── requirements.txt
├── Workflow.md
└── venv/
```

## Project Overview
Django-based academic management system for tracking student performance, attendance, and results.

## Tech Stack
- **Backend:** Django 4.x
- **Database:** SQLite (default)
- **Frontend:** HTML, CSS, JavaScript
- **QR Code:** python-qrcode

## Models

### 1. Subject
- `name`: CharField (100)
- `code`: CharField (20)

### 2. Teacher
- `first_name`, `last_name`: CharField
- `subject`: ForeignKey to Subject
- `email`: EmailField
- `joining_date`: DateField
- `phone`: CharField

### 3. Student
- `name`: CharField
- `roll_number`: CharField (unique)
- `student_class`, `section`: CharField
- `semester`: CharField
- `date_of_birth`: DateField
- `image`: ImageField
- `teacher`: ForeignKey to Teacher
- `qr_code_id`, `qr_code_data`: CharField (unique)

### 4. Result
- `student`: ForeignKey to Student
- `subject`: ForeignKey to Subject
- `terminal`: Choice (1st, 2nd, 3rd, Final)
- `marks_obtained`, `total_marks`: FloatField

### 5. Attendance
- `student`: ForeignKey to Student
- `date`, `time`: DateField/TimeField
- `qr_scanned`: BooleanField
- `device_info`, `ip_address`

## Application Flow

### Authentication
1. User visits `/login/`
2. Enters username/password
3. Django authenticates against User model
4. On success: redirect to `/dashboard/`
5. On failure: show error message

### Student Password Change
1. Student logs in and visits their dashboard
2. Clicks "Change Password" button
3. Modal opens with new password input
4. Enter new password and confirm
5. Password is updated via AJAX to `/change-password/`
6. Success/error message shown

### Student Login Flow
1. Student logs in with username matching their `name`
2. System searches Student records for name match
3. Redirects to `/student/<id>/` showing their own marks/attendance

### Add Marks Flow
1. Navigate to `/add-marks/`
2. Select student, subject, terminal
3. Enter marks_obtained and total_marks
4. If duplicate exists: updates existing record
5. Redirects to `/marks-list/`
6. Marks can be edited or deleted from the marks list

### QR Attendance Flow
1. Teacher/admin navigates to `/qr-scanner/`
2. Opens camera to scan student QR code
3. System parses QR data: `ACADSTAT_STUDENT|id|roll|name|qr_id`
4. Creates Attendance record for today
5. Returns success message

### Mark Sheet Generation
1. Navigate to `/mark-sheet/`
2. Select student and terminal
3. System calculates percentages and grades
4. Generates printable mark sheet

### Student Analysis
1. Navigate to `/student-analysis/`
2. Filter by: all, critical (<40%), warning (40-60%), attention (<60%)
3. Sort by: lowest, highest, name
4. View AI-generated summaries and recommendations

## URLs

| URL | View | Description |
|-----|------|--------------|
| `/` | home_view | Landing page |
| `/login/` | login_view | Login form (password visibility hidden by default) |
| `/logout/` | logout_view | Logout action |
| `/dashboard/` | dashboard | Admin dashboard |
| `/student/<id>/` | student_dashboard | Student view with password change |
| `/change-password/` | change_password | Student password change (AJAX) |
| `/add-marks/` | add_marks | Add/edit marks |
| `/marks-list/` | marks_list | View all marks |
| `/edit-marks/<id>/` | edit_marks | Edit marks |
| `/delete-marks/<id>/` | delete_marks | Delete marks |
| `/qr-codes/` | qr_codes | View all QR codes |
| `/qr-code/<id>/` | student_qr_code | Single QR code |
| `/qr-scanner/` | qr_scanner | Scan QR codes |
| `/process-qr-scan/` | process_qr_scan | Process scan |
| `/attendance-list/` | attendance_list | Attendance records |
| `/attendance-report/` | attendance_report | Attendance stats |
| `/chart-data/` | chart_data | API: chart data |
| `/mark-sheet/` | select_mark_sheet | Select for mark sheet |
| `/mark-sheet/<id>/<terminal>/` | mark_sheet | Generate mark sheet |
| `/student-analysis/` | student_analysis | Performance analysis |

## Management Commands

```bash
# Create student user
python manage.py create_student_user <name> <roll_number>

# Create all student users
python manage.py create_all_student_users

# List students
python manage.py list_students

# Send AI notifications to students (below threshold)
python manage.py send_notifications --threshold 60
python manage.py send_notifications --threshold 60 --dry-run  # Preview only
```

## Development Tasks

### Pending
- [ ] Export marks to CSV/Excel
- [ ] Bulk student import
- [ ] Parent portal
- [ ] Mobile app API

### In Progress
- [ ] Student QR code system
- [ ] Attendance tracking

### Completed
- [x] User authentication
- [x] Student password change
- [x] Dashboard with charts
- [x] Marks management
- [x] Result analysis
- [x] Mark sheet generation
- [x] Theme toggle (dark/light mode)
- [x] Login page password hidden by default

## Setup

```bash
# Clone and setup
cd djangoacadstat

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

## First Run Checklist
- [ ] Run migrations: `python manage.py migrate`
- [ ] Create superuser: `python manage.py createsuperuser`
- [ ] Add subjects via admin panel
- [ ] Add teachers via admin panel
- [ ] Add students via admin panel
- [ ] Login at `/login/`
- [ ] Add sample marks