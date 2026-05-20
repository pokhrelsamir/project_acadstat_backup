# -*- coding: utf-8 -*-
"""
Scheduler management command — polls Reminder + ScheduledTask records
and dispatches due items (notifications + emails).

Run in background:  python manage.py run_scheduler [--once]

Options:
  --once   Process due tasks once and exit (no continuous loop)
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

import time
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Run the reminder / scheduled-task scheduler poller"

    def add_arguments(self, parser):
        parser.add_argument(
            "--once",
            action="store_true",
            help="Process due tasks once and exit (no loop)",
        )
        parser.add_argument(
            "--interval",
            type=int,
            default=60,
            help="Polling interval in seconds (default: 60)",
        )

    # ── internal dispatchers ────────────────────────────────────────────────────

    def _dispatch_reminder(self, reminder: "Reminder"):
        """Create Notification + email for a reminder; handle recurrence."""
        from core.notification_service import NotificationService

        now = timezone.now()

        # Determine recipient
        title    = reminder.title
        message  = reminder.message
        notif_type = "info"

        if reminder.reminder_type == "attendance":
            notif_type = "warning"
        elif reminder.reminder_type == "assignment_deadline":
            notif_type = "warning"
        elif reminder.reminder_type == "fee":
            notif_type = "warning"
        else:
            notif_type = "info"

        # Notify student if linked
        if reminder.student:
            NotificationService.create_notification(
                recipient_student=reminder.student,
                title=title,
                message=message,
                notification_type=notif_type,
                priority="medium",
            )
            # Email
            if reminder.student.email:
                try:
                    from django.core.mail import send_mail
                    send_mail(
                        subject=f"Reminder: {title}",
                        message=f"Hi {reminder.student.name},\n\n{message}\n\n— AcadStat",
                        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@acadstat.local"),
                        recipient_list=[reminder.student.email],
                    )
                except Exception as exc:
                    logger.warning(f"Reminder email failed for {reminder.student.name}: {exc}")

            # Parent
            parent = getattr(reminder.student, "parent_info", None)
            if parent and parent.email:
                try:
                    from django.core.mail import send_mail
                    send_mail(
                        subject=f"Reminder: {title}",
                        message=f"Dear Parent,\n\n{message}\n\n— AcadStat",
                        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@acadstat.local"),
                        recipient_list=[parent.email],
                    )
                except Exception as exc:
                    logger.warning(f"Parent reminder email failed: {exc}")

        # Recurrence: push schedule forward
        if reminder.recurrence != "none":
            delta_map = {"daily": timedelta(days=1),
                         "weekly": timedelta(weeks=1),
                         "monthly": timedelta(days=30)}
            delta = delta_map.get(reminder.recurrence)
            if delta:
                reminder.scheduled_for = reminder.scheduled_for + delta
                if reminder.recurrence_until and reminder.scheduled_for.date() > reminder.recurrence_until:
                    reminder.is_active = False
                reminder.save()
                return  # do NOT mark as sent yet

        reminder.is_sent = True
        reminder.sent_at = now
        reminder.is_active = False
        reminder.save()

    def _dispatch_sms_digest(self, task: "ScheduledTask"):
        """Dispatch SMS/email digest task."""
        from core.notification_service import NotificationService

        payload = task.payload or {}
        student_id = payload.get("student_id")
        digest_type = payload.get("type", "weekly_attendance")

        try:
            from core.models import Student, Parent
            student = Student.objects.get(id=student_id)
        except (Student.DoesNotExist, ValueError, TypeError):
            logger.error(f"Invalid student_id in ScheduledTask {task.id}: {payload}")
            task.is_executed = True
            task.executed_at = timezone.now()
            task.save()
            return

        if digest_type == "weekly_attendance":
            NotificationService.send_weekly_attendance_digest(student)
        elif digest_type == "monthly_report":
            NotificationService.send_monthly_report(student)
        else:
            logger.warning(f"Unknown digest type: {digest_type}")

        task.is_executed = True
        task.executed_at = timezone.now()
        task.save()

    def _dispatch_fee_alert(self, task: "ScheduledTask"):
        """Fee alert: notify student + parent about overdue fee."""
        from core.notification_service import NotificationService

        payload = task.payload or {}
        student_id = payload.get("student_id")
        try:
            student = Student.objects.get(id=student_id)
        except (Student.DoesNotExist, ValueError, TypeError):
            logger.error(f"Invalid student_id in ScheduledTask {task.id}: {payload}")
            task.is_executed = True
            task.executed_at = timezone.now()
            task.save()
            return

        from core.models import Fee
        overdue = Fee.objects.filter(student=student, status="overdue")
        if overdue.exists():
            total = sum(f.balance for f in overdue)
            title   = f"Fees Overdue — {student.name}"
            message = (f"You have {overdue.count()} overdue fee(s) totalling "
                       f"Rs. {total:.2f}. Please clear it at the earliest.")
            NotificationService.create_notification(
                recipient_student=student, title=title, message=message,
                notification_type="warning", priority="high",
            )
            parent = getattr(student, "parent_info", None)
            if parent and parent.email:
                try:
                    from django.core.mail import send_mail
                    send_mail(
                        subject=title, message=message,
                        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@acadstat.local"),
                        recipient_list=[parent.email],
                    )
                except Exception as exc:
                    logger.warning(f"Fee alert email failed: {exc}")

        task.is_executed = True
        task.executed_at = timezone.now()
        task.save()

    def _dispatch_certificate_expiry(self, task: "ScheduledTask"):
        """Certificate expiry: notification stub — hook up to Certificate model when added."""
        task.is_executed = True
        task.executed_at = timezone.now()
        task.save()

    # ── main loop ───────────────────────────────────────────────────────────────

    def _process_due_tasks(self):
        """Query and dispatch all due tasks. Returns number dispatched."""
        from core.models import Reminder, ScheduledTask

        now = timezone.now()
        dispatched = 0

        # ── Reminders ───────────────────────────────────────────────────────────
        due_reminders = Reminder.objects.filter(
            is_active=True, is_sent=False, scheduled_for__lte=now
        ).select_related("teacher", "student", "subject")

        for rem in due_reminders:
            try:
                self._dispatch_reminder(rem)
                dispatched += 1
                logger.info(f"Reminder dispatched: {rem.title}")
            except Exception as exc:
                logger.error(f"Failed to dispatch reminder {rem.id}: {exc}", exc_info=True)

        # ── ScheduledTasks ──────────────────────────────────────────────────────
        due_tasks = ScheduledTask.objects.filter(
            is_active=True, is_executed=False, scheduled_for__lte=now
        )

        for task in due_tasks:
            try:
                dispatch_map = {
                    "reminder":             self._dispatch_reminder,
                    "sms_digest":           self._dispatch_sms_digest,
                    "fee_alert":            self._dispatch_fee_alert,
                    "certificate_expiry":   self._dispatch_certificate_expiry,
                }
                handler = dispatch_map.get(task.task_type)
                if handler:
                    handler(task)
                    dispatched += 1
                    logger.info(f"Task dispatched: {task.task_type} @ {task.scheduled_for}")
                else:
                    logger.warning(f"Unknown task type: {task.task_type}")
                    task.is_executed = True
                    task.executed_at = now
                    task.save()
            except Exception as exc:
                logger.error(f"Failed to dispatch task {task.id}: {exc}", exc_info=True)

        return dispatched

    def handle(self, *args, **options):
        once = options.get("once", False)
        interval = options.get("interval", 60)

        self.stdout.write(self.style.SUCCESS("Scheduler started."))

        if once:
            count = self._process_due_tasks()
            self.stdout.write(self.style.SUCCESS(f"Processed {count} task(s)."))
            return

        self.stdout.write(f"Polling every {interval}s. Press Ctrl+C to stop.")
        try:
            while True:
                count = self._process_due_tasks()
                if count:
                    self.stdout.write(
                        self.style.WARNING(f"[{timezone.now().strftime('%H:%M:%S')}] Dispatched {count} task(s).")
                    )
                time.sleep(interval)
        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS("\nScheduler stopped."))
