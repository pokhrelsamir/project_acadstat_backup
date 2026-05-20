"""
Management command: backup_db
Dump the current database to a JSON or pg_dump file.
Usage:
  python manage.py backup_db --output backups/
  python manage.py backup_db --output backups/ --format pg_dump
"""
import os
import subprocess
import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core import serializers


class Command(BaseCommand):
    help = "Create a database backup"

    def add_arguments(self, parser):
        parser.add_argument(
            '--output', '-o', type=str, default='backups',
            help='Output directory for backup files (default: backups/)'
        )
        parser.add_argument(
            '--format', '-f', type=str, default='json',
            choices=['json', 'pg_dump'],
            help='Backup format (default: json)'
        )

    def handle(self, *args, **options):
        output_dir = options['output']
        fmt = options['format']
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        os.makedirs(output_dir, exist_ok=True)

        db_engine = settings.DATABASES['default']['ENGINE']

        if fmt == 'pg_dump' and 'postgresql' in db_engine:
            filename = f"backup_{timestamp}.sql"
            filepath = os.path.join(output_dir, filename)
            db = settings.DATABASES['default']
            cmd = [
                'pg_dump',
                '-h', db.get('HOST', 'localhost'),
                '-p', str(db.get('PORT', 5432)),
                '-U', db['USER'],
                '-F', 'c',
                '-f', filepath,
                db['NAME'],
            ]
            env = os.environ.copy()
            env['PGPASSWORD'] = db['PASSWORD']
            try:
                subprocess.run(cmd, check=True, env=env, capture_output=True)
                self.stdout.write(self.style.SUCCESS(f"PostgreSQL backup saved: {filepath}"))
            except FileNotFoundError:
                self.stdout.write(self.style.WARNING("pg_dump not found — falling back to JSON."))
                self._json_backup(output_dir, timestamp)
        else:
            self._json_backup(output_dir, timestamp)

    def _json_backup(self, output_dir, timestamp):
        filename = f"backup_{timestamp}.json"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            # Serialize all models except Django internals
            models = [
                'core.Subject', 'core.EducationLevel', 'core.Semester',
                'core.AcademicYear', 'core.Department', 'core.GradeScale',
                'core.Teacher', 'core.Parent', 'core.Student',
                'core.StudentAcademicHistory', 'core.Attendance',
                'core.Assignment', 'core.AssignmentSubmission',
                'core.Exam', 'core.Fee', 'core.Announcement',
                'core.ActivityLog', 'core.TeacherEvaluation',
                'core.Notification', 'core.CourseMaterial',
                'core.Result', 'core.ResultLock', 'core.Message',
                'core.StudentNote', 'core.MLPrediction',
            ]
            serializers.serialize('json', self._iter_objects(models), stream=f, indent=2)
        self.stdout.write(self.style.SUCCESS(f"JSON backup saved: {filepath}"))

    def _iter_objects(self, model_labels):
        from django.apps import apps
        for label in model_labels:
            model = apps.get_model(label)
            for obj in model.objects.all():
                yield obj
