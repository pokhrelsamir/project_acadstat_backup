from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Teacher, Subject, Student
from django.db import transaction


class Command(BaseCommand):
    help = 'Create teacher accounts and assign subjects/students'

    def add_arguments(self, parser):
        parser.add_argument('--create-sample', action='store_true', help='Create sample teacher accounts')

    def handle(self, *args, **options):
        if options['create_sample']:
            self.create_sample_data()
        else:
            self.create_teacher_accounts()

    @transaction.atomic
    def create_sample_data(self):
        """Create sample teacher accounts with assignments"""
        self.stdout.write('Creating sample teacher accounts...')

        # Create subjects if they don't exist
        subjects_data = [
            {'name': 'Mathematics', 'code': 'MATH'},
            {'name': 'Physics', 'code': 'PHYS'},
            {'name': 'Chemistry', 'code': 'CHEM'},
            {'name': 'Biology', 'code': 'BIO'},
            {'name': 'Accountancy', 'code': 'ACC'},
        ]

        subjects = {}
        for subj_data in subjects_data:
            subj, created = Subject.objects.get_or_create(
                code=subj_data['code'],
                defaults={'name': subj_data['name']}
            )
            subjects[subj_data['code']] = subj
            if created:
                self.stdout.write(f'Created subject: {subj.name}')

        # Create teacher accounts for each subject
        teachers_data = [
            {
                'username': 'ram_sharma',
                'email': 'ram.sharma@school.com',
                'first_name': 'Ram',
                'last_name': 'Sharma',
                'subjects': ['PHYS'],  # Physics
            },
            {
                'username': 'prem_thapa',
                'email': 'prem.thapa@school.com',
                'first_name': 'Prem',
                'last_name': 'Thapa',
                'subjects': ['CHEM'],  # Chemistry
            },
            {
                'username': 'shyam_shah',
                'email': 'shyam.shah@school.com',
                'first_name': 'Shyam Kumar',
                'last_name': 'Shah',
                'subjects': ['BIO'],  # Biology
            },
            {
                'username': 'gita_tripathee',
                'email': 'gita.tripathee@school.com',
                'first_name': 'Gita',
                'last_name': 'Tripathee',
                'subjects': ['MATH'],  # Mathematics
            },
            {
                'username': 'guru_nayak',
                'email': 'guru.nayak@school.com',
                'first_name': 'Guru',
                'last_name': 'Nayak',
                'subjects': ['ACC'],  # Accountancy
            },
        ]

        for teacher_data in teachers_data:
            # Create user account
            user, user_created = User.objects.get_or_create(
                username=teacher_data['username'],
                defaults={
                    'email': teacher_data['email'],
                    'first_name': teacher_data['first_name'],
                    'last_name': teacher_data['last_name'],
                    'is_staff': False,
                    'is_active': True,
                }
            )

            if user_created:
                user.set_password('password123')  # Default password
                user.save()
                self.stdout.write(f'Created user account: {user.username}')

            # Create teacher profile
            teacher, teacher_created = Teacher.objects.get_or_create(
                user=user,
                defaults={
                    'first_name': teacher_data['first_name'],
                    'last_name': teacher_data['last_name'],
                    'email': teacher_data['email'],
                    'is_active': True,
                }
            )

            if teacher_created:
                self.stdout.write(f'Created teacher profile: {teacher.get_full_name()}')

            # Assign subjects
            for subj_code in teacher_data['subjects']:
                if subj_code in subjects:
                    teacher.subjects.add(subjects[subj_code])
                    self.stdout.write(f'Assigned {subjects[subj_code].name} to {teacher.get_full_name()}')

        self.stdout.write(self.style.SUCCESS('Teacher accounts created successfully!'))
        self.stdout.write('')
        self.stdout.write('Teacher Login Credentials:')
        self.stdout.write('-------------------------')
        for teacher_data in teachers_data:
            self.stdout.write(f"Username: {teacher_data['username']}")
            self.stdout.write(f"Password: password123")
            self.stdout.write(f"Email: {teacher_data['email']}")
            self.stdout.write('')
        self.stdout.write('Note: No students assigned yet. Admin can assign students to teachers via Django admin panel.')

    def create_teacher_accounts(self):
        """Interactive teacher account creation"""
        self.stdout.write('Teacher account creation utility')
        self.stdout.write('================================')

        username = input('Enter username: ').strip()
        if not username:
            self.stdout.write(self.style.ERROR('Username is required'))
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR('Username already exists'))
            return

        email = input('Enter email: ').strip()
        first_name = input('Enter first name: ').strip()
        last_name = input('Enter last name: ').strip()
        password = input('Enter password: ').strip()

        if not all([username, email, first_name, last_name, password]):
            self.stdout.write(self.style.ERROR('All fields are required'))
            return

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # Create teacher profile
        teacher = Teacher.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_active=True
        )

        self.stdout.write(self.style.SUCCESS(f'Teacher account created for {teacher.get_full_name()}'))
        self.stdout.write('Note: You need to assign subjects and students to this teacher via Django admin or programmatically')