from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from core.models import Student, Result, Parent, Attendance, Announcement, ActivityLog
from core.notification_service import NotificationService
from datetime import date
import logging

logger = logging.getLogger(__name__)
DEFAULT_PASSWORD = "password123"


@receiver(post_save, sender=Student)
def create_student_user(sender, instance, created, **kwargs):
    if created:
        if not User.objects.filter(username=instance.name).exists():
            user = User.objects.create_user(
                username=instance.name,
                password=DEFAULT_PASSWORD,
                first_name=instance.name.split()[0] if instance.name else '',
                last_name=' '.join(instance.name.split()[1:]) if len(instance.name.split()) > 1 else '',
                email=instance.email or ''
            )
            logger.info(f"Created user '{instance.name}'")
        else:
            logger.info(f"User '{instance.name}' already exists")

        # Auto-create a Parent stub if none exists
        if not hasattr(instance, 'parent_info'):
            Parent.objects.create(student=instance)


@receiver(post_delete, sender=Student)
def delete_student_user(sender, instance, **kwargs):
    try:
        user = User.objects.get(username=instance.name)
        user.delete()
        logger.info(f"Deleted user '{instance.name}'")
    except User.DoesNotExist:
        pass


@receiver(post_save, sender=Result)
def auto_alert_low_marks(sender, instance, created, **kwargs):
    """Auto-notify student when a newly-added result falls below passing threshold"""
    if created:
        gs = None
        try:
            from core.models import GradeScale
            gs = GradeScale.objects.filter(is_active=True).first()
        except Exception:
            pass
        if gs:
            pct = (instance.marks_obtained / instance.total_marks * 100) if instance.total_marks > 0 else 0
            if pct < gs.pass_mark_percent:
                NotificationService.create_notification(
                    recipient_student=instance.student,
                    title=f"⚠️ Low Score — {instance.subject.name}",
                    message=(
                        f"You scored {instance.marks_obtained}/{instance.total_marks} "
                        f"({pct:.1f}%) in {instance.subject.name} "
                        f"({instance.get_terminal_display()}). "
                        f"Please review this subject with your teacher."
                    ),
                    notification_type='warning',
                    priority='medium',
                    link_url='/student-dashboard/'
                )


@receiver(post_save, sender=Announcement)
def broadcast_announcement(sender, instance, created, **kwargs):
    """Send notifications to relevant audience when a new announcement is published"""
    if created and instance.is_published:
        from core.models import Student, Teacher
        if instance.audience == 'all':
            students = Student.objects.all()
            NotificationService.create_bulk_notifications(
                students,
                title=f"📢 {instance.title}",
                message=instance.content[:300],
                notification_type='info',
                priority=instance.priority if instance.priority != 'urgent' else 'high',
                link_url='/student-dashboard/'
            )
        elif instance.audience == 'students':
            students = Student.objects.all()
            NotificationService.create_bulk_notifications(
                students, title=f"📢 {instance.title}", message=instance.content[:300]
            )
        elif instance.audience == 'class' and instance.target_class:
            students = Student.objects.filter(student_class=instance.target_class)
            NotificationService.create_bulk_notifications(
                students, title=f"📢 {instance.title}", message=instance.content[:300]
            )
