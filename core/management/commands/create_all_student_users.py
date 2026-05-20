"""
Management command to create Django user accounts for ALL students.

Usage:
    python manage.py create_all_student_users --password student123

This creates Django user accounts for all students with the same password.
The username will be the student's name.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Student


class Command(BaseCommand):
    help = 'Create Django user accounts for all students'

    def add_arguments(self, parser):
        parser.add_argument(
            '--password',
            type=str,
            default='student123',
            help='Password for all student accounts (default: student123)'
        )
        parser.add_argument(
            '--prefix',
            type=str,
            default='',
            help='Add prefix to usernames (e.g., "student_" will make "student_ram")'
        )

    def handle(self, *args, **options):
        password = options['password']
        prefix = options['prefix']
        
        students = Student.objects.all()
        
        if not students.exists():
            self.stderr.write(self.style.WARNING('No students found in the database!'))
            return
        
        created_count = 0
        updated_count = 0
        
        for student in students:
            base_username = student.name.lower().replace(' ', '_')
            username = f"{prefix}{base_username}" if prefix else base_username
            
            # Handle duplicate usernames
            original_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{original_username}_{counter}"
                counter += 1
            
            if User.objects.filter(username=username).exists():
                # Update password for existing user
                user = User.objects.get(username=username)
                user.set_password(password)
                user.save()
                updated_count += 1
                self.stdout.write(f'  Updated: {username}')
            else:
                # Create new user
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    first_name=student.name.split()[0] if student.name else '',
                    last_name=' '.join(student.name.split()[1:]) if student.name else ''
                )
                created_count += 1
                self.stdout.write(f'  Created: {username}')
        
        self.stdout.write(self.style.SUCCESS(
            f'\n✓ Completed!'
            f'\n  Total students: {students.count()}'
            f'\n  New accounts created: {created_count}'
            f'\n  Accounts updated: {updated_count}'
            f'\n  Default password: {password}'
            f'\n\nStudents can login at: /login/'
            f'\nAfter login, they will be redirected to their personal dashboard.'
        ))
