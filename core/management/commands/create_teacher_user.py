"""
Management command to create a teacher user account for login.

Usage:
    python manage.py create_teacher_user <teacher_id> <password>

Example:
    python manage.py create_teacher_user 1 mypassword

This creates a Django user with username based on teacher's name
so they can login and see their own dashboard.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Teacher


class Command(BaseCommand):
    help = 'Create a Django user account for a teacher'

    def add_arguments(self, parser):
        parser.add_argument('teacher_id', type=int, help='Teacher ID')
        parser.add_argument('password', type=str, help='Password for the user')
        parser.add_argument('--username', type=str, help='Custom username (default: firstname_lastname)')

    def handle(self, *args, **options):
        teacher_id = options['teacher_id']
        password = options['password']
        custom_username = options.get('username')
        
        try:
            teacher = Teacher.objects.get(id=teacher_id)
        except Teacher.DoesNotExist:
            self.stderr.write(self.style.ERROR(f'Teacher with ID {teacher_id} not found!'))
            return
        
        # Generate username: remove spaces and make lowercase
        if custom_username:
            username = custom_username
        else:
            # Remove spaces from names for cleaner username
            first = teacher.first_name.replace(' ', '').lower()
            last = teacher.last_name.replace(' ', '').lower()
            username = f"{first}_{last}"
        
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
            email=teacher.email or '',
            first_name=teacher.first_name,
            last_name=teacher.last_name,
            is_staff=False,
            is_active=True
        )
        
        self.stdout.write(self.style.SUCCESS(
            f'Successfully created user account for {teacher.get_full_name()}!\n'
            f'  Username: {username}\n'
            f'  Teacher ID: {teacher_id}\n'
            f'  Login URL: /login/'
        ))
