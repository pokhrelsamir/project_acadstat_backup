"""
Management command to list all students with their IDs.

Usage:
    python manage.py list_students

This shows all students and their database IDs which you can use
with the create_student_user command.
"""
from django.core.management.base import BaseCommand
from core.models import Student


class Command(BaseCommand):
    help = 'List all students with their database IDs'

    def handle(self, *args, **options):
        students = Student.objects.all().order_by('id')
        
        if not students.exists():
            self.stdout.write(self.style.WARNING('No students found in the database!'))
            return
        
        self.stdout.write(self.style.SUCCESS('\n📋 All Students (Use ID in create_student_user command):\n'))
        self.stdout.write('-' * 50)
        
        for student in students:
            self.stdout.write(f'  ID: {student.id:3} | {student.name}')
        
        self.stdout.write('-' * 50)
        self.stdout.write(f'\nTotal: {students.count()} students\n')
        self.stdout.write('\nExamples:')
        self.stdout.write('  python manage.py create_student_user 1 mypassword')
        self.stdout.write('  python manage.py create_student_user 2 mypassword')
        self.stdout.write('\nOr create all at once:')
        self.stdout.write('  python manage.py create_all_student_users --password mypassword')
