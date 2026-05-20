"""
Management command: setup_rbac
Creates default RBAC roles in the database.
Usage: python manage.py setup_rbac
"""
from django.core.management.base import BaseCommand
from core.models import UserRole

DEFAULT_ROLES = [
    ('super_admin', 'Super Admin', 'Full system access including license management'),
    ('admin', 'Administrator', 'Manage students, teachers, subjects, fees, reports'),
    ('teacher', 'Teacher', 'Manage own subjects, students, attendance, assignments'),
    ('finance', 'Finance Officer', 'Manage fee records and invoicing'),
    ('librarian', 'Librarian', 'Manage course materials and announcements'),
    ('registrar', 'Registrar', 'Manage student records and academic history'),
    ('viewer', 'Viewer', 'Read-only access to dashboard and reports'),
]

PERMISSIONS = {
    'super_admin': dict(can_manage_students=True, can_manage_teachers=True,
                        can_manage_subjects=True, can_manage_fees=True,
                        can_manage_exams=True, can_manage_attendance=True,
                        can_manage_materials=True, can_view_reports=True,
                        can_manage_system=True),
    'admin': dict(can_manage_students=True, can_manage_teachers=True,
                  can_manage_subjects=True, can_manage_fees=True,
                  can_manage_exams=True, can_manage_attendance=True,
                  can_manage_materials=True, can_view_reports=True,
                  can_manage_system=False),
    'teacher': dict(can_manage_students=False, can_manage_teachers=False,
                    can_manage_subjects=True, can_manage_fees=False,
                    can_manage_exams=True, can_manage_attendance=True,
                    can_manage_materials=True, can_view_reports=True,
                    can_manage_system=False),
    'finance': dict(can_manage_students=False, can_manage_teachers=False,
                    can_manage_subjects=False, can_manage_fees=True,
                    can_manage_exams=False, can_manage_attendance=False,
                    can_manage_materials=False, can_view_reports=True,
                    can_manage_system=False),
    'librarian': dict(can_manage_students=False, can_manage_teachers=False,
                      can_manage_subjects=False, can_manage_fees=False,
                      can_manage_exams=False, can_manage_attendance=False,
                      can_manage_materials=True, can_view_reports=True,
                      can_manage_system=False),
    'registrar': dict(can_manage_students=True, can_manage_teachers=False,
                      can_manage_subjects=False, can_manage_fees=False,
                      can_manage_exams=False, can_manage_attendance=False,
                      can_manage_materials=False, can_view_reports=True,
                      can_manage_system=False),
    'viewer': dict(can_manage_students=False, can_manage_teachers=False,
                   can_manage_subjects=False, can_manage_fees=False,
                   can_manage_exams=False, can_manage_attendance=False,
                   can_manage_materials=False, can_view_reports=True,
                   can_manage_system=False),
}


class Command(BaseCommand):
    help = "Create default RBAC roles"

    def handle(self, *args, **options):
        created = 0
        for code, name, description in DEFAULT_ROLES:
            role, was_created = UserRole.objects.get_or_create(
                code=code,
                defaults={
                    'name': name,
                    'description': description,
                    'is_system_role': True,
                    **PERMISSIONS.get(code, {}),
                },
            )
            if was_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(f"  Created role: {name} ({code})"))
            else:
                # Update permissions if role already exists
                for perm_field, value in PERMISSIONS.get(code, {}).items():
                    setattr(role, perm_field, value)
                role.save(update_fields=list(PERMISSIONS.get(code, {}).keys()))
                self.stdout.write(self.style.WARNING(f"  Updated role: {name} ({code})"))
        self.stdout.write(self.style.SUCCESS(f"Done — {created} new roles created."))
