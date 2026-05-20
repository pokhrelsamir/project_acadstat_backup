"""
Email Service — wraps Django's send_mail with logging and template support.
"""
import logging
from django.core.mail import send_mail as django_send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone

logger = logging.getLogger(__name__)


def send_mail(subject, body, recipient_list, html_message=None, from_email=None):
    """Send an email via Django's backend, catching and logging exceptions."""
    if not recipient_list:
        logger.warning("send_mail called with empty recipient_list — skipping.")
        return False
    try:
        django_send_mail(
            subject=subject,
            message=body,
            from_email=from_email or settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            html_message=html_message or body,
            fail_silently=False,
        )
        logger.info("Email sent to %s — subject: %s", recipient_list, subject)
        return True
    except Exception as exc:
        logger.exception("send_mail failed to %s: %s", recipient_list, exc)
        try:
            from core.models import ActivityLog
            ActivityLog.objects.create(
                user=None,
                action='other',
                description=f"Email send failed to {recipient_list}: {exc}",
                metadata={'subject': subject, 'recipients': recipient_list, 'error': str(exc)},
            )
        except Exception:
            pass
        return False


def send_template_mail(template_name, context, recipient_list, subject, from_email=None):
    """Render an HTML template from core/emails/ and send it."""
    try:
        html = render_to_string(f"core/emails/{template_name}", context)
    except Exception as exc:
        logger.exception("Template rendering failed for %s: %s", template_name, exc)
        return False
    return send_mail(
        subject=subject,
        body="Notification",
        recipient_list=recipient_list,
        html_message=html,
        from_email=from_email,
    )


def notify_student(student, title, message, link_url='', notification_type='info'):
    """Create a Notification record and send an email if student has an email."""
    from core.models import Notification
    Notification.objects.create(
        recipient=student,
        title=title,
        message=message,
        notification_type=notification_type,
        priority='medium',
        link_url=link_url,
    )
    try:
        from core.notification_service import NotificationService
        NotificationService.log_activity(
            user=None,
            action='add_announcement',
            description=f"Sent notification to {student.name}: {title}",
        )
    except Exception:
        pass
    if student.email:
        send_mail(
            subject=title,
            body=message,
            recipient_list=[student.email],
        )
    return True


def notify_parent(parent, title, message):
    """Send email to a parent (no Notification record in DB, just email)."""
    if parent.email:
        return send_mail(subject=title, body=message, recipient_list=[parent.email])
    logger.warning("Parent %s has no email — cannot send notification.", parent)
    return False


def notify_teachers_bulk(teachers, title, message):
    """Send email to all teachers in a queryset or list."""
    emails = []
    for t in teachers:
        if t.email:
            emails.append(t.email)
    if not emails:
        logger.warning("No teachers have valid emails for bulk notification.")
        return 0
    sent = send_mail(subject=title, body=message, recipient_list=emails)
    return len(emails) if sent else 0
