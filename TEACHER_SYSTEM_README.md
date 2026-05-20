# Teacher Authentication System

This system provides role-based access control for teachers in the Academic System.

## Features

### For Teachers
- **Restricted Access**: Teachers can only access data for subjects and students assigned to them
- **Add Marks**: Only for their assigned subjects and students
- **Bulk Upload**: Restricted to their subjects/students
- **View Marks**: Only marks for their subjects/students
- **Generate Mark Sheets**: For their assigned subjects
- **Course Materials**: Upload/manage materials for their subjects
- **Student QR Codes**: View QR codes for their students
- **QR Scanner**: Mark attendance for their students
- **Attendance Reports**: View attendance data for their students

### For Admins
- Full access to all system features
- Create and manage teacher accounts
- Assign subjects and students to teachers
- Monitor all teacher activities

## Setup Instructions

1. **Apply Migrations**
   ```bash
   python manage.py migrate
   ```

2. **Run Setup Script**
   ```bash
   python setup_teachers.py
   ```
   This will create sample teacher accounts and sample data.

3. **Access the System**
   - Admin: Login at `/admin/` (create superuser if needed)
   - Teachers: Login at `/` with their credentials

## Sample Teacher Accounts

| Username | Password | Subjects | Students |
|----------|----------|----------|----------|
| teacher_math | password123 | Mathematics | John, Jane, Charlie, Diana |
| teacher_science | password123 | Physics, Chemistry, Biology | Bob, Alice |
| teacher_cs | password123 | Computer Science, English | All students |

## Teacher Dashboard Features

1. **Dashboard Overview**
   - Statistics for assigned subjects/students
   - Quick access to all teacher functions
   - Recent student list

2. **Marks Management**
   - Add individual marks (restricted to assigned subjects/students)
   - Bulk upload via Excel (restricted)
   - View marks (filtered to teacher's data)
   - Edit existing marks

3. **Course Materials**
   - Upload files or external links
   - Organize by subject
   - Share with students

4. **Attendance System**
   - QR code generation for students
   - QR scanning for attendance
   - Attendance reports and analytics

## Security Features

- **Subject Restrictions**: Teachers cannot add/view marks for unassigned subjects
- **Student Restrictions**: Teachers cannot access data for unassigned students
- **File Upload Security**: Teachers can only upload materials for their subjects
- **Role-based Redirects**: Automatic redirection based on user role

## Admin Management

### Creating Teacher Accounts
1. Go to Django Admin → Users → Add User
2. Create user account with credentials
3. Go to Teachers → Add Teacher
4. Link the user account and assign subjects/students

### Assigning Subjects/Students
- Use the Django admin interface
- Teachers can have multiple subjects
- Students can be assigned to multiple teachers
- All assignments are enforced in the application logic

## API Endpoints

All existing API endpoints now include teacher permission checks:
- `/api/student-info/<id>/` - Only for teacher's students
- QR scanning endpoints - Only for teacher's students

## Database Changes

- **Teacher Model**: Added OneToOneField to User, ManyToManyField for subjects/students
- **Student Model**: Changed teacher field to teachers (ManyToManyField)
- **CourseMaterial Model**: New model for file/link uploads
- **Permission Checks**: All views now check teacher permissions

## Usage Examples

### As a Teacher
1. Login with teacher credentials
2. View dashboard with assigned data
3. Add marks only for assigned subjects/students
4. Upload materials for assigned subjects
5. Scan QR codes for assigned students

### As an Admin
1. Login with admin credentials
2. Manage all system data
3. Create/assign teacher accounts
4. Monitor teacher activities
5. Override any restrictions if needed

## Troubleshooting

- **Teacher can't access data**: Check subject/student assignments in admin
- **Permission denied errors**: Verify teacher account is active and properly configured
- **Login issues**: Ensure teacher accounts are created with proper User linking

## Future Enhancements

- Email notifications for teachers
- Advanced reporting and analytics
- Mobile app integration
- Parent-teacher communication features