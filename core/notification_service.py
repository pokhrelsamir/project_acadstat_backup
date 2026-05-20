"""
Notification Service for sending alerts to students, parents and teachers
"""
import logging
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Q
from django.urls import reverse

logger = logging.getLogger(__name__)

class NotificationService:
    """Service class to handle notifications for students"""

    @staticmethod
    def create_notification(
        recipient_student,
        title,
        message,
        notification_type='info',
        priority='medium',
        sender=None,
        link_url=None
    ):
        from core.models import Notification

        notification = Notification.objects.create(
            recipient=recipient_student,
            title=title,
            message=message,
            notification_type=notification_type,
            priority=priority,
            sender=sender,
            link_url=link_url
        )
        logger.info(f"Notification created: {title} for {recipient_student.name if recipient_student else 'Bulk'}")
        return notification

    @staticmethod
    def create_bulk_notifications(students, title, message, notification_type='info', priority='medium', sender=None, link_url=None):
        notifications = []
        for student in students:
            notification = NotificationService.create_notification(
                recipient_student=student,
                title=title,
                message=message,
                notification_type=notification_type,
                priority=priority,
                sender=sender,
                link_url=link_url
            )
            notifications.append(notification)
        return notifications

    @staticmethod
    def get_student_notifications(student, unread_only=False, limit=50):
        from core.models import Notification
        qs = Notification.objects.filter(recipient=student).exclude(
            Q(material__isnull=True, title__startswith='New Material:') |
            Q(material__is_active=False)
        )
        if unread_only:
            qs = qs.filter(is_read=False)
        return qs.order_by('-created_at')[:limit]

    @staticmethod
    def mark_as_read(notification_id, student):
        from core.models import Notification
        try:
            notification = Notification.objects.get(id=notification_id, recipient=student)
            notification.is_read = True
            notification.read_at = timezone.now()
            notification.save()
            return True
        except Notification.DoesNotExist:
            return False

    @staticmethod
    def mark_all_as_read(student):
        from core.models import Notification
        Notification.objects.filter(recipient=student, is_read=False).update(
            is_read=True, read_at=timezone.now()
        )
        return True

    @staticmethod
    def get_unread_count(student):
        from core.models import Notification
        return Notification.objects.filter(recipient=student, is_read=False).exclude(
            Q(material__isnull=True, title__startswith='New Material:') |
            Q(material__is_active=False)
        ).count()

    @staticmethod
    def notify_course_material_upload(material, teacher):
        from core.models import Student, Notification
        students = Student.objects.all()
        if not students.exists():
            return []
        title = f"New Material: {material.title}"
        message = (
            f"Your teacher has uploaded new course material for {material.subject.name}.\n\n"
            f"📄 {material.title}\n"
            f"📝 {material.description[:100]}{'...' if material.description and len(material.description) > 100 else ''}\n"
            f"📅 Uploaded: {material.upload_date.strftime('%b %d, %Y')}\n\n"
            f"Check your course materials section for details."
        )
        link_url = "/view-materials/"
        notifications = []
        for student in students:
            notification = Notification.objects.create(
                recipient=student, title=title, message=message,
                notification_type='info', priority='medium',
                sender=teacher, link_url=link_url, material=material
            )
            notifications.append(notification)
        logger.info(f"Created {len(notifications)} notifications for material: {material.title}")
        return notifications

    # ─── Smart Auto-Alerts ────────────────────────────────────────────────────

    @staticmethod
    def check_and_alert_low_marks(result, threshold=40):
        """Alert student when a new mark falls below threshold %"""
        from core.models import Student, Notification
        if result.total_marks > 0:
            pct = (result.marks_obtained / result.total_marks) * 100
        else:
            pct = 0
        if pct < threshold:
            student = result.student
            title = f"⚠️ Low Score Alert — {result.subject.name}"
            message = (
                f"You scored {result.marks_obtained}/{result.total_marks} "
                f"({pct:.1f}%) in {result.subject.name} ({result.get_terminal_display()}). "
                f"Consider reviewing this subject with your teacher."
            )
            Notification.objects.create(
                recipient=student,
                title=title,
                message=message,
                notification_type='warning',
                priority='high',
                link_url="/student-dashboard/"
            )

    @staticmethod
    def alert_parent_low_attendance(student, threshold=75):
        """Alert parent/guardian if student attendance drops below threshold %"""
        from core.models import Notification
        pct = student.attendance_percentage
        if pct < threshold:
            parent = getattr(student, 'parent_info', None)
            if parent and parent.phone:
                # Log the alert — integrate SMS gateway here when available
                logger.warning(f"LOW ATTENDANCE: {student.name} ({pct}%) — Parent: {parent.phone}")
            # Create system log entry
            title = f"📋 Attendance Alert — {student.name}"
            Notification.objects.create(
                recipient=student,
                title=title,
                message=f"Your attendance is currently at {pct}%. Please maintain regular attendance.",
                notification_type='warning',
                priority='medium',
                link_url="/student-dashboard/"
            )

    @staticmethod
    def send_result_published_notification(teacher, target_students, terminal='Final'):
        """Notify students when results are published"""
        title = f"✅ Results Published — {terminal} Terminal"
        message = (
            f"Your {terminal} terminal results have been published. "
            f"Log in to your dashboard to view your marks and performance analytics."
        )
        NotificationService.create_bulk_notifications(
            target_students, title=title, message=message,
            notification_type='success', priority='medium', sender=teacher,
        )

    @staticmethod
    def log_activity(user, action, description='', ip_address=None, metadata=None):
        """Record system activity"""
        from core.models import ActivityLog
        ActivityLog.objects.create(
            user=user,
            action=action,
            description=description,
            ip_address=ip_address,
            metadata=metadata or {}
        )

    @staticmethod
    def send_email(subject, body, recipient_email):
        """Send an email notification; uses email_service when not console backend."""
        if 'console' not in settings.EMAIL_BACKEND:
            try:
                from core.email_service import send_mail
                send_mail(subject, body, [recipient_email])
                return True
            except Exception as exc:
                logger.exception("Email send failed to %s: %s", recipient_email, exc)
                return False
        else:
            logger.info("Console email backend — would send to %s: %s", recipient_email, subject)
            return True

    # ═══════════════════════════════════════════════════════════════════════════════
    # A12  AUTOMATED DIGESTS
    # ═══════════════════════════════════════════════════════════════════════════════

    @staticmethod
    def send_weekly_attendance_digest(student):
        """Compute weekly attendance % and email the student + parent"""
        from datetime import date, timedelta
        today = date.today()
        week_start = today - timedelta(days=today.weekday())

        records = student.attendance_records.filter(date__gte=week_start)
        total = records.count()
        present = records.filter(status='present').count()
        pct = round((present / total) * 100, 1) if total else 0

        subject = f"Your Weekly Attendance Digest — {student.name}"
        body = (
            f"Hi {student.name},\n\n"
            f"Here is your attendance summary for the week of "
            f"{week_start.strftime('%b %d')} – {today.strftime('%b %d, %Y')}:\n\n"
            f"  📅 Days tracked : {total}\n"
            f"  ✅ Present      : {present}\n"
            f"  ❌ Absent/Late  : {total - present}\n"
            f"  📊 Attendance % : {pct}%\n"
            f"\nKeep it up!\n\n"
            f"— Academic Management System"
        )
        recipients = [student.email] if student.email else []
        parent = getattr(student, 'parent_info', None)
        if parent and parent.email:
            recipients.append(parent.email)
        if recipients:
            try:
                send_mail(subject, body, None, recipients)
            except Exception as exc:
                logger.warning(f"Weekly attendance digest mail failed for {student.name}: {exc}")

    @staticmethod
    def send_monthly_report(student):
        """Monthly marks avg + attendance + fee outstanding — emailed to student + parent"""
        from datetime import date
        from core.models import Attendance, Fee

        today = date.today()
        month_name = today.strftime('%B %Y')

        # Attendance
        attend_records = student.attendance_records.filter(
            date__year=today.year, date__month=today.month
        )
        total_att = attend_records.count()
        present_att = attend_records.filter(status='present').count()
        att_pct = round((present_att / total_att) * 100, 1) if total_att else 0

        # Marks
        results = student.result_set.all()
        if results.exists():
            total_marks = sum(r.marks_obtained for r in results)
            grand_total = sum(r.total_marks for r in results)
            avg = round((total_marks / grand_total) * 100, 1) if grand_total else 0
        else:
            avg = 0

        # Fee
        outstanding = Fee.objects.filter(student=student, status__in=['pending', 'overdue'])
        fee_due = sum(f.balance for f in outstanding) if outstanding.exists() else 0

        subject = f"Your AcadStat Report – {month_name}"
        body = (
            f"Hi {student.name},\n\n"
            f"This is your monthly academic summary for {month_name}.\n\n"
            f"  📊 Average Marks     : {avg}%\n"
            f"  📅 Attendance %      : {att_pct}%\n"
            f"  💰 Fee Outstanding   : ₹{fee_due:.2f}\n"
            f"\nContact your class teacher for any questions.\n\n"
            f"— Academic Management System"
        )
        recipients = [student.email] if student.email else []
        parent = getattr(student, 'parent_info', None)
        if parent and parent.email:
            recipients.append(parent.email)
        if recipients:
            try:
                send_mail(subject, body, None, recipients)
            except Exception as exc:
                logger.warning(f"Monthly report mail failed for {student.name}: {exc}")
