"""
Management command to create a student user account for login.

Usage:
    python manage.py create_student_user <student_id> <password>

Example:
    python manage.py create_student_user 1 password123

This creates a Django user with the student's name as username
so they can login and see their own dashboard.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Student


class Command(BaseCommand):
    help = 'Create a Django user account for a student'

    def add_arguments(self, parser):
        parser.add_argument('student_id', type=int, help='Student ID')
        parser.add_argument('password', type=str, help='Password for the user')
        parser.add_argument('--username', type=str, help='Custom username (default: student name)')

    def handle(self, *args, **options):
        student_id = options['student_id']
        password = options['password']
        custom_username = options.get('username')
        
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            self.stderr.write(self.style.ERROR(f'Student with ID {student_id} not found!'))
            return
        
        # Use custom username or default to student name
        username = custom_username or student.name
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            self.stderr.write(self.style.WARNING(f'User "{username}" already exists!'))
            # Update the password
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Updated password for user "{username}"'))
            return
        
        # Create new user
        user = User.objects.create_user(
            username=username,
            password=password,
            email=options.get('email', ''),
            first_name=student.name.split()[0] if student.name else '',
            last_name=' '.join(student.name.split()[1:]) if student.name else ''
        )
        
        self.stdout.write(self.style.SUCCESS(
            f'Successfully created user account for {student.name}!\n'
            f'  Username: {username}\n'
            f'  Student ID: {student_id}\n'
            f'  Login URL: /login/'
        ))
