from django.contrib.auth import views as auth_views
from django.urls import path
from core import views
from core import views_excel

app_name = "core"

urlpatterns = [
    # ── Core ──────────────────────────────────────────────────────────────────
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('change-password/', views.change_password, name='change_password'),

    # ── Global Search ─────────────────────────────────────────────────────────
    path('search/', views.global_search, name='global_search'),
    path('api/search/', views.api_search, name='api_search'),

    # ── Marks ─────────────────────────────────────────────────────────────────
    path('add-marks/', views.add_marks, name='add_marks'),
    path('marks-list/', views.marks_list, name='marks_list'),
    path('edit-marks/<int:mark_id>/', views.edit_marks, name='edit_marks'),
    path('delete-marks/<int:mark_id>/', views.delete_marks, name='delete_marks'),
    path('api/results/', views.api_results, name='api_results'),
    path('api/results/<int:result_id>/', views.api_result_detail, name='api_result_detail'),
    path('api/students/', views.api_students, name='api_students'),

    # ── Result Lock ───────────────────────────────────────────────────────────
    path('lock-result/<int:result_id>/', views.lock_result, name='lock_result'),
    path('unlock-result/<int:result_id>/', views.unlock_result, name='unlock_result'),
    path('lock-all-results/', views.lock_all_results, name='lock_all_results'),

    # ── Mark Sheet ────────────────────────────────────────────────────────────
    path('mark-sheet/', views.mark_sheet, name='mark_sheet'),
    path('mark-sheet/<int:student_id>/<str:terminal>/', views.mark_sheet, name='mark_sheet_terminal'),
    path('mark-sheet/<int:student_id>/', views.mark_sheet, name='mark_sheet_student'),
    path('mark-sheet/pdf/<int:student_id>/<str:terminal>/', views.export_mark_sheet_pdf, name='export_mark_sheet_pdf'),
    path('select-mark-sheet/', views.select_mark_sheet, name='select_mark_sheet'),

    # ── Student Analysis ──────────────────────────────────────────────────────
    path('student-analysis/', views.student_analysis, name='student_analysis'),
    path('api/student-info/<int:student_id>/', views.student_info, name='student_info'),
    path('api/student-chart/<int:student_id>/', views.student_chart_data, name='student_chart'),

    # ── AI & Analytics ────────────────────────────────────────────────────────
    path('ai-recommendations/', views.ai_recommendations, name='ai_recommendations'),
    path('performance-heatmap/', views.performance_heatmap, name='performance_heatmap'),
    path('improvement-tracking/', views.improvement_tracking, name='improvement_tracking'),
    path('ai-context-help/', views.ai_contextual_help, name='ai_contextual_help'),
    path('ml-predict/', views.create_ml_prediction, name='create_ml_prediction'),
    path('ml-predictions/', views.get_ml_predictions, name='get_ml_predictions'),
    path('milestone-check/', views.milestone_check, name='milestone_check'),

    # ── Charts ────────────────────────────────────────────────────────────────
    path('chart-data/', views.chart_data, name='chart_data'),

    # ── Course Materials ──────────────────────────────────────────────────────
    path('course-materials/', views.course_materials, name='course_materials'),
    path('view-materials/', views.view_course_materials, name='view_caterials'),
    path('delete-material/<int:material_id>/', views.delete_course_material, name='delete_course_material'),
    path('notes/', views.student_notes_view, name='student_notes'),
    path('notes/add/', views.add_student_note, name='add_student_note'),
    path('notes/share/', views.share_note, name='share_note'),
    path('notes/delete/<int:note_id>/', views.delete_student_note, name='delete_student_note'),
    path('notes/class-share/', views.teacher_share_note_with_class, name='teacher_share_note'),

    # ── Notifications ─────────────────────────────────────────────────────────
    path('api/student-notifications/', views.student_notifications, name='student_notifications'),
    path('api/mark-notification-read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('api/mark-all-notifications-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),

    # ── Teacher ───────────────────────────────────────────────────────────────
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teachers-list/', views.teachers_list_view, name='teachers_list'),
    path('teacher-performance/', views.teacher_performance, name='teacher_performance'),
    path('teacher-workload/', views.workload_analytics, name='workload_analytics'),
    path('teacher-evaluation/<int:teacher_id>/', views.teacher_evaluation_view, name='teacher_evaluation'),
    path('teacher-messages/', views.teacher_messages, name='teacher_messages'),
    path('teacher-messages/inbox/', views.teacher_messages_inbox, name='teacher_messages_inbox'),

    # ── Students ──────────────────────────────────────────────────────────────
    path('students-list/', views.students_list_view, name='students_list'),
    path('add-student/', views.add_student_view, name='add_student'),
    path('edit-student/<int:student_id>/', views.edit_student_view, name='edit_student'),
    path('bulk-import-students/', views.bulk_import_students, name='bulk_import_students'),
    path('promote-students/', views.promote_students, name='promote_students'),
    path('student-history/<int:student_id>/', views.student_history, name='student_history'),
    path('manage-parent/<int:student_id>/', views.manage_parent, name='manage_parent'),
    path('profile/', views.profile_view, name='profile'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('export-students-excel/', views.export_students_excel, name='export_students_excel'),

    # ── Smart Analytics ───────────────────────────────────────────────────────
    path('smart-dashboard/', views.smart_dashboard, name='smart_dashboard'),

    # ── Messaging ─────────────────────────────────────────────────────────────
    path('student-messages/', views.student_messages, name='student_messages'),
    path('send-message/', views.send_student_message, name='send_student_message'),
    path('parent-message/', views.student_parent_message, name='student_parent_message'),

    # ── Attendance ────────────────────────────────────────────────────────────
    path('attendance/', views.attendance_view, name='attendance'),
    path('attendance-report/', views.attendance_report, name='attendance_report'),

    # ── Assignments ───────────────────────────────────────────────────────────
    path('assignments/', views.assignments_view, name='assignments'),
    path('assignment/<int:assignment_id>/', views.assignment_detail_view, name='assignment_detail'),
    path('student-assignments/', views.student_assignments_view, name='student_assignments'),
    path('submit-assignment/<int:assignment_id>/', views.submit_assignment, name='submit_assignment'),

    # ── Exams ─────────────────────────────────────────────────────────────────
    path('exam-schedule/', views.exam_schedule_view, name='exam_schedule'),
    path('exam-schedule-student/', views.exam_schedule_student, name='exam_schedule_student'),

    # ── Fees ──────────────────────────────────────────────────────────────────
    path('fee-management/', views.fee_management, name='fee_management'),
    path('my-fees/', views.student_fee_view, name='student_fee'),

    # ── Announcements ─────────────────────────────────────────────────────────
    path('announcements/', views.announcements_view, name='announcements'),
    path('announcements-student/', views.student_announcements_view, name='student_announcements'),

    # ── Config ────────────────────────────────────────────────────────────────
    path('grade-scale-config/', views.grade_scale_config, name='grade_scale_config'),
    path('academic-year-config/', views.academic_year_config, name='academic_year_config'),

    # ── Logs ──────────────────────────────────────────────────────────────────
    path('activity-logs/', views.activity_logs, name='activity_logs'),

    # ── Excel Upload ──────────────────────────────────────────────────────────
    path('upload-marks/', views_excel.upload_marks_excel, name='upload_marks_excel'),
    path('download-excel-template/', views_excel.download_excel_template, name='download_excel_template'),

    # ── Admin Export All ──────────────────────────────────────────────────────
    path('export-all/', views.admin_export_all, name='admin_export_all'),

    # ══════════════════════════════════════════════════════════════════════════
    # A3 — INVOICE BILLING / SUBSCRIPTION MODULE
    # ══════════════════════════════════════════════════════════════════════════
    path('subscriptions/', views.subscription_management, name='subscription_management'),
    path('invoices/', views.invoice_list, name='invoice_list'),
    path('invoices/create/', views.invoice_create, name='invoice_create'),
    path('invoices/<str:invoice_number>/', views.invoice_detail, name='invoice_detail'),
    path('invoices/<str:invoice_number>/pdf/', views.invoice_pdf, name='invoice_pdf'),
    path('invoices/<int:invoice_id>/mark-paid/', views.invoice_mark_paid, name='invoice_mark_paid'),

    # ══════════════════════════════════════════════════════════════════════════
    # A8 — ANALYTICS EXPORT BUNDLE
    # ══════════════════════════════════════════════════════════════════════════
    path('smart-dashboard/pdf/', views.export_smart_dashboard_pdf, name='export_smart_dashboard_pdf'),
    path('smart-dashboard/excel/', views.export_smart_dashboard_excel, name='export_smart_dashboard_excel'),

    # ══════════════════════════════════════════════════════════════════════════
    # A9 — CERTIFICATE GENERATOR
    # ══════════════════════════════════════════════════════════════════════════
    path('certificates/templates/', views.certificate_templates, name='certificate_templates'),
    path('certificates/generate/', views.generate_certificate, name='generate_certificate'),
    path('certificates/', views.certificate_list, name='certificate_list'),
    path('certificates/<str:cert_number>/', views.certificate_view, name='certificate_view'),
    path('certificates/<str:cert_number>/pdf/', views.certificate_pdf, name='certificate_pdf'),
    path('certificates/verify/', views.verify_certificate, name='verify_certificate'),

    # ══════════════════════════════════════════════════════════════════════════
    # A14 — API KEY & WEBHOOK SYSTEM (DEVELOPER PORTAL)
    # ══════════════════════════════════════════════════════════════════════════
    path('developer/', views.developer_portal, name='developer_portal'),
    path('developer/api-keys/', views.manage_api_keys, name='manage_api_keys'),
    path('developer/webhooks/', views.manage_webhooks, name='manage_webhooks'),
    path('developer/api-docs/', views.api_docs, name='api_docs'),

    # ══════════════════════════════════════════════════════════════════════════
    # A5 — SUPPORT TICKET SYSTEM
    # ══════════════════════════════════════════════════════════════════════════
    path('tickets/', views.ticket_list, name='ticket_list'),
    path('tickets/create/', views.ticket_create, name='ticket_create'),
    path('tickets/<str:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('tickets/<str:ticket_id>/update/', views.ticket_update_status, name='ticket_update_status'),
    path('tickets/<str:ticket_id>/comment/', views.ticket_comment, name='ticket_comment'),

    # ══════════════════════════════════════════════════════════════════════════
    # A10 — SSO (GOOGLE / MICROSOFT / GITHUB)
    # ══════════════════════════════════════════════════════════════════════════
    path('sso/google/', views.sso_login, name='sso_google'),
    path('sso/google/callback/', views.sso_callback, name='sso_google_callback'),
    path('sso/microsoft/', views.sso_microsoft, name='sso_microsoft'),
    path('sso/microsoft/callback/', views.sso_microsoft_callback, name='sso_microsoft_callback'),
    path('sso/github/', views.sso_github, name='sso_github'),
    path('sso/github/callback/', views.sso_github_callback, name='sso_github_callback'),
    path('sso/status/', views.sso_status, name='sso_status'),

    # ── T8  Smart Question Bank ────────────────────────────────────────────
    path('question-bank/', views.question_bank, name='question_bank'),
    path('question-bank/add/', views.question_bank_add, name='question_bank_add'),
    path('question-bank/import/', views.question_bank_import, name='question_bank_import'),
    path('question-bank/<int:qid>/edit/', views.question_bank_edit, name='question_bank_edit'),
    path('question-bank/<int:qid>/delete/', views.question_bank_delete, name='question_bank_delete'),
    path('paper-templates/', views.paper_template_list, name='paper_template_list'),
    path('paper-templates/create/', views.paper_template_create, name='paper_template_create'),
    path('paper-templates/<int:tid>/generate/', views.paper_template_generate, name='paper_template_generate'),

    # ── T9  Reminder Scheduler ─────────────────────────────────────────────
    path('reminders/', views.reminder_list, name='reminder_list'),
    path('reminders/create/', views.reminder_create, name='reminder_create'),
    path('reminders/<int:reminder_id>/delete/', views.reminder_delete, name='reminder_delete'),
    path('admin/scheduled-tasks/', views.scheduled_tasks_list, name='scheduled_tasks_list'),

    # ── T10 Subject Analytics ──────────────────────────────────────────────
    path('subject-analytics/', views.subject_analytics, name='subject_analytics'),

    # ── A12 Automated Digests ──────────────────────────────────────────────
    path('admin/trigger-weekly-digest/', views.trigger_weekly_digest, name='trigger_weekly_digest'),
    path('admin/trigger-monthly-report/', views.trigger_monthly_report, name='trigger_monthly_report'),
]
