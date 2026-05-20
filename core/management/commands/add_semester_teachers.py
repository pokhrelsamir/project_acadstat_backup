"""
Management command to add semester professors with their subjects and user accounts.

Usage:
    python manage.py add_semester_teachers

This creates Teacher profiles and associated User accounts for the following professor-subject mappings:
    1st semester: C Programming -> Govinda Prasad Bhattarai
    2nd semester: Object Oriented Programming -> Sumitra Phyual
    3rd semester: Statistics -> Suraj Bhatta
    4th semester: DBMS -> Chandi Prasad Pandey
    5th semester: Multimedia Computing -> Renu Maharjan

All bachelor-level teachers are assigned all three education levels (School, College, Bachelor) 
so they can add marks for any level. They also get the specific semester assignment.

Default password for all accounts: password123

After running this, use `python manage.py list_teacher` to see the teachers.
You can change passwords via Django admin or using `python manage.py create_teacher_user <id> <new_password>`.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Teacher, Subject, EducationLevel, Semester


class Command(BaseCommand):
    help = 'Add semester professors with their assigned subjects and user accounts'

    def handle(self, *args, **options):
        self.stdout.write('Adding semester professors with user accounts, levels, and semesters...\n')

        # Define professor-subject mappings with semester info
        professors_data = [
            {
                'first_name': 'Govinda Prasad',
                'last_name': 'Bhattarai',
                'subject_name': 'C Programming',
                'subject_code': 'CP',
                'semester': 1,
                'username': 'govinda_bhattarai',
                'email': 'govinda.bhattarai@college.edu',
            },
            {
                'first_name': 'Sumitra',
                'last_name': 'Phyual',
                'subject_name': 'Object Oriented Programming',
                'subject_code': 'OOP',
                'semester': 2,
                'username': 'sumitra_phyual',
                'email': 'sumitra.phyual@college.edu',
            },
            {
                'first_name': 'Suraj',
                'last_name': 'Bhatta',
                'subject_name': 'Statistics',
                'subject_code': 'STAT',
                'semester': 3,
                'username': 'suraj_bhatta',
                'email': 'suraj.bhatta@college.edu',
            },
            {
                'first_name': 'Chandi Prasad',
                'last_name': 'Pandey',
                'subject_name': 'DBMS',
                'subject_code': 'DBMS',
                'semester': 4,
                'username': 'chandi_pandey',
                'email': 'chandi.pandey@college.edu',
            },
            {
                'first_name': 'Renu',
                'last_name': 'Maharjan',
                'subject_name': 'Multimedia Computing',
                'subject_code': 'MMCP',
                'semester': 5,
                'username': 'renu_maharjan',
                'email': 'renu.maharjan@college.edu',
            },
        ]

        created_count = 0
        updated_count = 0
        default_password = 'password123'

        # Ensure EducationLevel instances exist
        level_codes = ['school', 'college', 'bachelor']
        levels = {}
        for code in level_codes:
            level, created = EducationLevel.objects.get_or_create(
                code=code,
                defaults={'name': dict(EducationLevel.LEVEL_CHOICES)[code]}
            )
            levels[code] = level
            if created:
                self.stdout.write(f'Created education level: {level.name}')

        # Ensure Semester instances (1-8) exist
        semesters = {}
        for num in range(1, 9):
            sem, created = Semester.objects.get_or_create(
                number=num,
                defaults={'label': f'Semester {num}'}
            )
            semesters[num] = sem
            if created:
                self.stdout.write(f'Created semester: {sem}')

        for prof in professors_data:
            # Create or get subject
            subject, subject_created = Subject.objects.get_or_create(
                code=prof['subject_code'],
                defaults={'name': prof['subject_name']}
            )
            if subject_created:
                self.stdout.write(f'Created subject: {subject.name} ({subject.code})')
            else:
                self.stdout.write(f'Found existing subject: {subject.name}')

            # Create or get user account
            user, user_created = User.objects.get_or_create(
                username=prof['username'],
                defaults={
                    'email': prof['email'],
                    'first_name': prof['first_name'],
                    'last_name': prof['last_name'],
                    'is_active': True,
                }
            )
            if user_created:
                user.set_password(default_password)
                user.save()
                self.stdout.write(f'Created user: {user.username} (password: {default_password})')
            else:
                self.stdout.write(f'User already exists: {user.username}')

            # Create or get teacher profile linked to this user
            teacher, teacher_created = Teacher.objects.get_or_create(
                user=user,
                defaults={
                    'first_name': prof['first_name'],
                    'last_name': prof['last_name'],
                    'email': prof['email'],
                    'is_active': True,
                }
            )
            if teacher_created:
                created_count += 1
                self.stdout.write(f'Created teacher: {teacher.get_full_name()}')
            else:
                updated_count += 1
                self.stdout.write(f'Teacher already exists: {teacher.get_full_name()}')

            # Assign all three education levels to bachelor teachers
            teacher.levels.set([levels['school'], levels['college'], levels['bachelor']])
            self.stdout.write(f'Assigned levels: School, College, Bachelor to {teacher.get_full_name()}')

            # Assign specific semester
            sem_num = prof['semester']
            teacher.semesters.add(semesters[sem_num])
            self.stdout.write(f'Assigned Semester {sem_num} to {teacher.get_full_name()}')

            # Assign subject to teacher (if not already assigned)
            if not teacher.subjects.filter(id=subject.id).exists():
                teacher.subjects.add(subject)
                self.stdout.write(f'Assigned {subject.name} to {teacher.get_full_name()}')
            else:
                self.stdout.write(f'{subject.name} already assigned to {teacher.get_full_name()}')

            self.stdout.write('')

        self.stdout.write(self.style.SUCCESS(
            f'Completed! Created {created_count} new teachers, {updated_count} already existed.\n'
            f'Total teachers: {Teacher.objects.count()}\n\n'
            'Teacher login credentials:\n'
            '-------------------------\n'
            'Default password for all: password123\n\n'
            'All bachelor-level teachers have been assigned School, College, and Bachelor levels, '
            'plus their specific semester (1-5).\n\n'
            'To change a password for a teacher, use:\n'
            '  python manage.py create_teacher_user <teacher_id> <new_password>\n\n'
            'To list all teachers with their IDs:\n'
            '  python manage.py list_teacher\n'
            'To view/edit teacher levels and semesters, use Django admin.'
        ))
