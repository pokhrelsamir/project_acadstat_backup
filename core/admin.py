from django.contrib import admin
from .models import (
    Student, Subject, Result, Teacher, CourseMaterial,
    EducationLevel, Semester, AcademicYear, Department,
    GradeScale, Parent, StudentAcademicHistory, Attendance,
    Assignment, AssignmentSubmission, Exam, Fee,
    Announcement, ActivityLog, TeacherEvaluation, Notification,
    ResultLock, Message, StudentNote, MLPrediction,
    LicenseKey, SystemConfig, UserRole, UserProfile,
    SystemBackup, ParentUser, ResultPublishSession, ResultSessionEntry,
    Subscription, Invoice, CertificateTemplate, Certificate,
    APIKey, WebhookEndpoint, WebhookDeliveryLog,
    SupportTicket, TicketComment, SSOProvider,
    LessonPlan, SyllabusCoverage,
    GradingRubric, RubricCriterion, RubricScoreEntry, RubricTemplate,
    OnlineExam, Question, ExamAttempt, ExamAnswer,
    ExamSeatingPlan, SeatAllocation,
    TeacherLeave,
    QuestionBank, QuestionPaperTemplate, Reminder, ScheduledTask,
)

# ── Inline helpers ────────────────────────────────────────────────────────────

class StudentInline(admin.TabularInline):
    model = Student
    extra = 0
    fields = ('name', 'roll_number', 'level', 'student_class', 'section', 'phone', 'email')
    show_change_link = True


class AssignmentSubmissionInline(admin.TabularInline):
    model = AssignmentSubmission
    extra = 0
    fields = ('student', 'status', 'marks_obtained', 'submitted_at')
    readonly_fields = ('submitted_at',)


class StudentAcademicHistoryInline(admin.TabularInline):
    model = StudentAcademicHistory
    extra = 0
    fields = ('academic_year', 'previous_class', 'promoted_to_class', 'percentage', 'grade')
    readonly_fields = ('academic_year', 'previous_class', 'promoted_to_class', 'percentage', 'grade')


class ParentInline(admin.StackedInline):
    model = Parent
    extra = 0
    fields = ('father_name', 'mother_name', 'guardian_name', 'phone', 'email', 'address', 'relation')
    can_delete = False


class FeeInline(admin.TabularInline):
    model = Fee
    extra = 0
    fields = ('fee_type', 'amount', 'amount_paid', 'due_date', 'status')
    readonly_fields = ('status',)


# ── Model admin registrations ────────────────────────────────────────────────

@admin.register(EducationLevel)
class EducationLevelAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    ordering = ('code',)


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('number', 'label')
    ordering = ('number',)
    list_filter = ('number',)


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'is_current')
    list_editable = ('is_current',)
    ordering = ('-start_date',)
    list_filter = ('is_current',)
    search_fields = ('name',)
    fieldsets = (
        (None, {'fields': ('name', ('start_date', 'end_date'), 'is_current')}),
    )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'head', 'is_active')
    list_editable = ('is_active',)
    ordering = ('name',)
    search_fields = ('name', 'code')
    list_filter = ('is_active',)
    autocomplete_fields = ('head',)


@admin.register(GradeScale)
class GradeScaleAdmin(admin.ModelAdmin):
    list_display = ('name', 'pass_mark_percent', 'is_active', 'created_at')
    list_editable = ('pass_mark_percent', 'is_active')
    ordering = ('name',)
    search_fields = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'pass_mark_percent', 'description', 'is_active'),
            'description': 'Grade scale determines how raw % is converted to grades (A+, A, B+ … F).'
        }),
    )


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        'get_full_name', 'email', 'department', 'role', 'is_active', 'joining_date',
        'get_subjects_count', 'get_students_count', 'get_levels_display',
        'get_semesters_display', 'is_admin'
    )
    search_fields = ('first_name', 'last_name', 'email', 'user__username')
    list_filter = ('is_active', 'is_admin', 'joining_date', 'subjects', 'levels', 'semesters', 'department')
    ordering = ('first_name',)
    readonly_fields = ('user',)
    filter_horizontal = ('subjects', 'levels', 'semesters')
    fieldsets = (
        ('User Account', {'fields': ('user', 'is_active', 'is_admin')}),
        ('Personal Information', {'fields': ('first_name', 'last_name', 'email', 'phone', 'joining_date')}),
        ('Department', {'fields': ('department',)}),
        ('Assignments', {'fields': ('subjects',)}),
        ('Education Levels', {
            'fields': ('levels',),
            'description': 'Select the education levels this teacher can teach. Bachelor level teachers should also select School and College levels for full access.'
        }),
        ('Semester Assignments (for Bachelor Level)', {
            'fields': ('semesters',),
            'description': 'Select the semesters this teacher teaches (only applicable for Bachelor level).',
            'classes': ('collapse',),
        }),
    )

    class Media:
        js = ('js/teacher_admin.js',)

    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Full Name'

    def get_subjects_count(self, obj):
        return obj.subjects.count()
    get_subjects_count.short_description = 'Subjects'

    def get_students_count(self, obj):
        return obj.students.count()
    get_students_count.short_description = 'Students'

    def get_levels_display(self, obj):
        return ", ".join([level.name for level in obj.levels.all()]) or "-"
    get_levels_display.short_description = 'Levels'

    def get_semesters_display(self, obj):
        return ", ".join([f"Sem {sem.number}" for sem in obj.semesters.all()]) or "-"
    get_semesters_display.short_description = 'Semesters'


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'roll_number', 'level', 'student_class', 'section',
        'semester', 'phone', 'email', 'attendance_percentage',
        'get_teachers_count', 'get_parent_count',
    )
    search_fields = ('name', 'roll_number', 'phone', 'email')
    list_filter = ('level', 'student_class', 'section', 'semester', 'academic_year', 'teachers', 'is_promoted')
    ordering = ('student_class', 'name')
    filter_horizontal = ('teachers',)
    inlines = [ParentInline, StudentAcademicHistoryInline, FeeInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'roll_number', 'level', 'student_class', 'section',
                       'semester', 'date_of_birth', 'gender', 'blood_group',
                       'admission_date', 'academic_year', 'house', 'scholarship', 'is_promoted')
        }),
        ('Contact & Image', {
            'fields': ('email', 'phone', 'emergency_contact', 'image')
        }),
        ('Assignments', {'fields': ('teachers',)}),
    )
    list_per_page = 100

    class Media:
        js = ('js/student_admin.js',)

    def get_teachers_count(self, obj):
        return obj.teachers.count()
    get_teachers_count.short_description = 'Teachers'

    def get_parent_count(self, obj):
        return 1 if hasattr(obj, 'parent_info') else 0
    get_parent_count.short_description = 'Parent'


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('get_student_name', 'father_name', 'guardian_name', 'phone', 'email', 'relation')
    search_fields = ('student__name', 'father_name', 'guardian_name', 'phone', 'email')
    list_filter = ('relation', 'is_primary_contact')
    ordering = ('student__name',)
    autocomplete_fields = ('student',)

    def get_student_name(self, obj):
        return obj.student.name
    get_student_name.short_description = 'Student'


@admin.register(StudentAcademicHistory)
class StudentAcademicHistoryAdmin(admin.ModelAdmin):
    list_display = ('student', 'academic_year', 'previous_class', 'promoted_to_class', 'percentage', 'grade')
    list_filter = ('academic_year', 'grade')
    search_fields = ('student__name', 'previous_class', 'promoted_to_class')
    ordering = ('-academic_year__start_date',)
    readonly_fields = ('student', 'previous_class', 'promoted_to_class', 'percentage', 'grade')
    date_hierarchy = 'created_at'


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'date', 'status', 'recorded_by', 'remarks')
    list_filter = ('date', 'status', 'subject', 'recorded_by')
    search_fields = ('student__name',)
    ordering = ('-date', 'student__name')
    date_hierarchy = 'date'
    list_per_page = 200
    list_select_related = ('student', 'subject', 'recorded_by')


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'subject', 'teacher', 'target_class', 'target_section',
        'due_date', 'total_marks', 'is_published', 'priority', 'submissions_count',
    )
    list_filter = ('subject', 'target_class', 'is_published', 'priority', 'due_date')
    search_fields = ('title', 'subject__name', 'teacher__first_name', 'teacher__last_name')
    ordering = ('-due_date',)
    filter_horizontal = ('target_students',)
    inlines = [AssignmentSubmissionInline]
    date_hierarchy = 'due_date'


@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'assignment', 'status', 'score_percentage', 'submitted_at', 'graded_at')
    list_filter = ('status', 'assignment__subject', 'assignment__target_class')
    search_fields = ('student__name', 'assignment__title')
    ordering = ('-submitted_at',)
    readonly_fields = ('submitted_at', 'score_percentage')
    autocomplete_fields = ('student', 'assignment')


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'exam_type', 'subject', 'target_class', 'target_section',
        'exam_date', 'start_time', 'total_marks', 'passing_marks', 'is_published',
    )
    list_filter = ('exam_type', 'subject', 'target_class', 'exam_date', 'is_published')
    search_fields = ('title', 'subject__name', 'venue')
    ordering = ('exam_date',)
    date_hierarchy = 'exam_date'


@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ('student', 'fee_type', 'amount', 'amount_paid', 'balance', 'due_date', 'status')
    list_filter = ('status', 'fee_type', 'due_date')
    search_fields = ('student__name', 'receipt_number')
    ordering = ('-due_date',)
    readonly_fields = ('balance',)
    autocomplete_fields = ('student', 'created_by')


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'audience', 'priority', 'is_published', 'published_by', 'published_at', 'expires_at')
    list_filter = ('audience', 'priority', 'is_published')
    search_fields = ('title', 'content')
    ordering = ('-published_at',)
    list_editable = ('is_published',)
    actions = ['make_published']
    date_hierarchy = 'published_at'

    @admin.action(description='Publish selected announcements')
    def make_published(self, request, queryset):
        for ann in queryset:
            ann.is_published = True
            if not ann.published_at:
                ann.published_at = timezone.now()
            ann.save()


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'description', 'timestamp', 'ip_address')
    list_filter = ('action', 'timestamp', 'user')
    search_fields = ('user__username', 'description')
    ordering = ('-timestamp',)
    readonly_fields = ('user', 'action', 'description', 'ip_address', 'timestamp', 'metadata')
    date_hierarchy = 'timestamp'


@admin.register(TeacherEvaluation)
class TeacherEvaluationAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'evaluator', 'academic_year', 'overall_score', 'created_at')
    list_filter = ('academic_year', 'overall_score', 'teacher__department')
    search_fields = ('teacher__first_name', 'teacher__last_name', 'evaluator__username')
    ordering = ('-created_at',)
    readonly_fields = ('overall_score',)
    autocomplete_fields = ('teacher', 'evaluator')
    date_hierarchy = 'created_at'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'recipient', 'notification_type', 'priority', 'is_read', 'created_at', 'sender')
    list_filter = ('notification_type', 'priority', 'is_read', 'created_at')
    search_fields = ('title', 'recipient__name', 'message')
    ordering = ('-created_at',)
    list_editable = ('is_read',)
    readonly_fields = ('title', 'recipient', 'message', 'notification_type', 'priority',
                        'created_at', 'read_at', 'sender')
    date_hierarchy = 'created_at'


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'total_marks', 'pass_marks', 'is_practical')
    search_fields = ('name', 'code')
    ordering = ('name',)
    fieldsets = (
        (None, {'fields': ('name', 'code', 'total_marks', 'pass_marks', 'is_practical')}),
    )


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'terminal', 'marks_obtained', 'total_marks', 'percentage', 'grade', 'created_at')
    list_filter = ('subject', 'terminal', 'created_at')
    search_fields = ('student__name', 'subject__name')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'


@admin.register(CourseMaterial)
class CourseMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'teacher', 'upload_date', 'is_active', 'get_file_type')
    list_filter = ('subject', 'teacher', 'upload_date', 'is_active')
    search_fields = ('title', 'description', 'subject__name', 'teacher__first_name', 'teacher__last_name')
    ordering = ('-upload_date',)
    date_hierarchy = 'upload_date'
    readonly_fields = ('upload_date',)

    def get_file_type(self, obj):
        if obj.file:
            return 'File Upload'
        elif obj.file_url:
            return 'External Link'
        return 'None'
    get_file_type.short_description = 'Type'

from datetime import datetime


# ── Result Lock ───────────────────────────────────────────────────────────────

@admin.register(ResultLock)
class ResultLockAdmin(admin.ModelAdmin):
    list_display = ('result', 'locked_by', 'locked_at', 'reason')
    list_filter = ('locked_at', 'locked_by')
    search_fields = ('result__student__name', 'result__subject__name', 'reason')
    ordering = ('-locked_at',)
    readonly_fields = ('result', 'locked_by', 'locked_at')


# ── Messages ─────────────────────────────────────────────────────────────────

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sender_display', 'recipient_display', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('subject', 'user', 'sender__first_name', 'recipient_student__name')
    ordering = ('-created_at',)
    readonly_fields = ('sender', 'sender_student', 'recipient_student', 'recipient_teacher', 'created_at')

    def sender_display(self, obj):
        return obj.sender.get_full_name() if obj.sender else (obj.sender_student.name if obj.sender_student else '-')
    sender_display.short_description = 'Sender'

    def recipient_display(self, obj):
        return obj.recipient_student.name if obj.recipient_student else (obj.recipient_teacher.get_full_name() if obj.recipient_teacher else '-')
    recipient_display.short_description = 'Recipient'


# ── Student Notes ─────────────────────────────────────────────────────────────

@admin.register(StudentNote)
class StudentNoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'student', 'priority', 'created_by', 'created_at')
    list_filter = ('priority', 'created_at', 'created_by')
    search_fields = ('title', 'content', 'student__name')
    ordering = ('-created_at',)
    autocomplete_fields = ('student',)
    list_editable = ('priority',)


# ── ML Predictions ────────────────────────────────────────────────────────────

@admin.register(MLPrediction)
class MLPredictionAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'predicted_grade', 'confidence_score', 'actual_grade', 'created_at')
    list_filter = ('predicted_grade', 'subject', 'model_version', 'created_at')
    search_fields = ('student__name', 'subject__name')
    ordering = ('-created_at',)
    autocomplete_fields = ('student', 'subject')
    readonly_fields = ('created_at',)


# ═════════════════════════════════════════════════════════════════════════════
#  A2 — LICENSE KEY SYSTEM
# ═════════════════════════════════════════════════════════════════════════════

@admin.register(LicenseKey)
class LicenseKeyAdmin(admin.ModelAdmin):
    list_display = ('institution_name', 'key_short', 'max_teachers', 'max_students',
                    'current_teachers', 'current_students', 'is_active', 'expires_at', 'issued_at')
    list_filter = ('is_active', 'expires_at', 'issued_at')
    search_fields = ('institution_name', 'key')
    ordering = ('-issued_at',)
    readonly_fields = ('key', 'issued_at', 'current_teachers', 'current_students', 'current_branches')
    actions = ['activate_keys', 'deactivate_keys']
    fieldsets = (
        (None, {'fields': ('institution_name', 'key', 'is_active', 'expires_at', 'notes')}),
        ('Limits', {'fields': ('max_teachers', 'max_students', 'max_branches')}),
        ('Usage (auto-computed)', {'fields': ('current_teachers', 'current_students', 'current_branches')}),
        ('Meta', {'fields': ('created_by', 'issued_at')}),
    )

    def key_short(self, obj):
        return obj.key[:16] + '...'
    key_short.short_description = 'Key'

    @admin.action(description='Activate selected licenses (deactivates all others)')
    def activate_keys(self, request, queryset):
        LicenseKey.objects.update(is_active=False)
        queryset.update(is_active=True)
        self.message_user(request, 'Selected licenses activated (others deactivated).')

    @admin.action(description='Deactivate selected licenses')
    def deactivate_keys(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, 'Selected licenses deactivated.')


@admin.register(SystemConfig)
class SystemConfigAdmin(admin.ModelAdmin):
    list_display = ('key', 'value_short', 'updated_at')
    search_fields = ('key', 'value')
    ordering = ('key',)
    readonly_fields = ('updated_at',)

    def value_short(self, obj):
        return obj.value[:80]
    value_short.short_description = 'Value'


# ═════════════════════════════════════════════════════════════════════════════
#  A6 — RBAC 2.0 ROLE & PERMISSION MANAGER
# ═════════════════════════════════════════════════════════════════════════════

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_system_role',
                    'can_manage_students', 'can_manage_teachers', 'can_manage_subjects',
                    'can_manage_fees', 'can_manage_exams', 'can_manage_attendance',
                    'can_manage_materials', 'can_view_reports', 'can_manage_system')
    list_filter = ('is_system_role', 'code')
    search_fields = ('name', 'code', 'description')
    ordering = ('code',)
    list_editable = ()
    readonly_fields = ('is_system_role',)
    fieldsets = (
        (None, {'fields': ('name', 'code', 'description', 'is_system_role')}),
        ('Permissions', {
            'fields': ('can_manage_students', 'can_manage_teachers', 'can_manage_subjects',
                       'can_manage_fees', 'can_manage_exams', 'can_manage_attendance',
                       'can_manage_materials', 'can_view_reports', 'can_manage_system'),
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'branch')
    list_filter = ('role', 'branch')
    search_fields = ('user__username', 'user__first_name', 'role__name')
    ordering = ('user__username',)
    autocomplete_fields = ('user', 'role', 'branch')


# ═════════════════════════════════════════════════════════════════════════════
#  A7 — BACKUP & RESTORE
# ═════════════════════════════════════════════════════════════════════════════

@admin.register(SystemBackup)
class SystemBackupAdmin(admin.ModelAdmin):
    list_display = ('filename', 'backup_type', 'size_display', 'status', 'triggered_by', 'created_at')
    list_filter = ('status', 'backup_type', 'created_at')
    search_fields = ('filename', 'triggered_by__username')
    ordering = ('-created_at',)
    readonly_fields = ('filename', 'size_bytes', 'backup_type', 'triggered_by', 'created_at')


# ═════════════════════════════════════════════════════════════════════════════
#  A11 — PARENT USER PORTAL
# ═════════════════════════════════════════════════════════════════════════════

@admin.register(ParentUser)
class ParentUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'parent_student', 'phone', 'is_verified', 'created_at')
    list_filter = ('is_verified', 'created_at')
    search_fields = ('user__username', 'parent__student__name', 'phone')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    autocomplete_fields = ('user', 'parent')

    def parent_student(self, obj):
        return obj.parent.student.name
    parent_student.short_description = 'Student'


# ═════════════════════════════════════════════════════════════════════════════
#  A13 — RESULT PUBLICATION WORKFLOW
# ═════════════════════════════════════════════════════════════════════════════

class ResultSessionEntryInline(admin.TabularInline):
    model = ResultSessionEntry
    extra = 0
    fields = ('result', 'is_locked')
    autocomplete_fields = ('result',)


@admin.register(ResultPublishSession)
class ResultPublishSessionAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'target_class', 'status', 'created_by',
                    'reviewed_by', 'approved_by', 'published_at', 'created_at')
    list_filter = ('status', 'subject', 'target_class', 'academic_year', 'created_at')
    search_fields = ('name', 'subject__name', 'target_class', 'rejection_reason')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    autocomplete_fields = ('subject', 'academic_year', 'created_by', 'reviewed_by', 'approved_by')
    inlines = [ResultSessionEntryInline]
    fieldsets = (
        (None, {'fields': ('name', 'subject', 'target_class', 'academic_year', 'status')}),
        ('Workflow', {'fields': ('created_by', 'reviewed_by', 'approved_by', 'published_at', 'rejection_reason')}),
        ('Meta', {'fields': ('created_at',)}),
    )


@admin.register(ResultSessionEntry)
class ResultSessionEntryAdmin(admin.ModelAdmin):
    list_display = ('session', 'result_student', 'result_subject', 'is_locked')
    list_filter = ('is_locked', 'session__status', 'result__subject')
    search_fields = ('result__student__name', 'result__subject__name', 'session__name')
    autocomplete_fields = ('session', 'result')
    ordering = ('session', 'result__student__name')

    def result_student(self, obj):
        return obj.result.student.name
    result_student.short_description = 'Student'

    def result_subject(self, obj):
        return obj.result.subject.name
    result_subject.short_description = 'Subject'



# ═════════════════════════════════════════════════════════════════════════════
# T2 — LESSON PLAN & SYLLABUS TRACKER
# ═════════════════════════════════════════════════════════════════════════════

@admin.register(LessonPlan)
class LessonPlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'subject', 'class_section', 'chapter_topic', 'planned_date', 'status', 'teaching_method')
    list_filter = ('subject', 'teacher', 'status', 'class_section', 'teaching_method', 'planned_date')
    search_fields = ('title', 'chapter_topic', 'class_section', 'teacher__first_name', 'teacher__last_name')
    ordering = ('-planned_date',)
    date_hierarchy = 'planned_date'
    list_select_related = ('teacher', 'subject')


@admin.register(SyllabusCoverage)
class SyllabusCoverageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'class_section', 'chapter_name', 'planned_order', 'estimated_hours',
                    'actual_hours', 'completion_pct', 'is_completed')
    list_filter = ('subject', 'class_section', 'is_completed')
    search_fields = ('chapter_name', 'class_section', 'subject__name')
    ordering = ('subject__name', 'class_section', 'planned_order')
    list_editable = ('actual_hours', 'is_completed')
    list_select_related = ('subject',)


# ═════════════════════════════════════════════════════════════════════════════
# T3 — TWO-WAY GRADING RUBRICS
# ═════════════════════════════════════════════════════════════════════════════

class RubricCriterionInline(admin.TabularInline):
    model = RubricCriterion
    extra = 1
    fields = ('name', 'max_score', 'weight_percent', 'order')
    ordering = ('order',)


@admin.register(GradingRubric)
class GradingRubricAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'subject', 'is_active', 'created_at', 'get_criteria_count')
    list_filter = ('subject', 'teacher', 'is_active', 'created_at')
    search_fields = ('name', 'description', 'teacher__first_name', 'teacher__last_name')
    ordering = ('-created_at',)
    inlines = [RubricCriterionInline]
    list_select_related = ('teacher', 'subject')

    def get_criteria_count(self, obj):
        return obj.criteria.count()
    get_criteria_count.short_description = 'Criteria Count'


@admin.register(RubricCriterion)
class RubricCriterionAdmin(admin.ModelAdmin):
    list_display = ('name', 'rubric', 'max_score', 'weight_percent', 'order')
    list_filter = ('rubric__teacher', 'rubric__subject')
    search_fields = ('name', 'rubric__name')
    ordering = ('rubric__name', 'order')
    list_select_related = ('rubric',)


@admin.register(RubricScoreEntry)
class RubricScoreEntryAdmin(admin.ModelAdmin):
    list_display = ('submission', 'criterion', 'score_obtained', 'criterion_max')
    list_filter = ('submission__assignment__subject',)
    search_fields = ('submission__student__name', 'criterion__name')
    ordering = ('-created_at',)
    list_select_related = ('submission__student', 'criterion', 'submission__assignment')
    readonly_fields = ('created_at',)

    def criterion_max(self, obj):
        return obj.criterion.max_score
    criterion_max.short_description = 'Max Score'


@admin.register(RubricTemplate)
class RubricTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_global', 'created_at')
    list_filter = ('is_global', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)
    readonly_fields = ('created_at',)


# ═════════════════════════════════════════════════════════════════════════════
# T4 — ONLINE EXAM / QUIZ MODULE
# ═════════════════════════════════════════════════════════════════════════════

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0
    fields = ('order', 'question_text', 'question_type', 'marks', 'correct_answer')
    ordering = ('order',)


@admin.register(OnlineExam)
class OnlineExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'teacher', 'target_class', 'total_marks', 'passing_marks',
                    'duration_minutes', 'start_at', 'end_at', 'is_published', 'max_attempts')
    list_filter = ('subject', 'teacher', 'target_class', 'is_published', 'start_at')
    search_fields = ('title', 'subject__name', 'target_class')
    ordering = ('-start_at',)
    inlines = [QuestionInline]
    date_hierarchy = 'start_at'
    list_select_related = ('subject', 'teacher')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('order', 'online_exam', 'question_type', 'marks', 'correct_answer')
    list_filter = ('question_type', 'online_exam__subject')
    search_fields = ('question_text', 'online_exam__title')
    ordering = ('online_exam', 'order')
    list_select_related = ('online_exam', 'online_exam__subject')


@admin.register(ExamAttempt)
class ExamAttemptAdmin(admin.ModelAdmin):
    list_display = ('student', 'online_exam', 'attempt_number', 'status', 'score_obtained', 'started_at', 'submitted_at')
    list_filter = ('status', 'online_exam__subject', 'online_exam__target_class', 'started_at')
    search_fields = ('student__name', 'online_exam__title')
    ordering = ('-started_at',)
    readonly_fields = ('started_at', 'submitted_at')
    list_select_related = ('student', 'online_exam')


@admin.register(ExamAnswer)
class ExamAnswerAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'question', 'selected_option', 'marks_awarded')
    list_filter = ('attempt__online_exam__subject',)
    search_fields = ('attempt__student__name', 'question__question_text')
    ordering = ('-created_at',)
    list_select_related = ('attempt__student', 'question')


# ═════════════════════════════════════════════════════════════════════════════
# T5 — SEATING PLAN & HALL TICKET GENERATOR
# ═════════════════════════════════════════════════════════════════════════════

@admin.register(ExamSeatingPlan)
class ExamSeatingPlanAdmin(admin.ModelAdmin):
    list_display = ('room_name', 'exam', 'teacher', 'room_capacity', 'arrangement_type', 'created_at', 'get_allocation_count')
    list_filter = ('exam__subject', 'teacher', 'room_name', 'arrangement_type', 'created_at')
    search_fields = ('room_name', 'exam__title', 'teacher__first_name', 'teacher__last_name')
    ordering = ('-created_at',)
    list_select_related = ('exam', 'teacher')

    def get_allocation_count(self, obj):
        return obj.allocations.count()
    get_allocation_count.short_description = 'Allocations'


@admin.register(SeatAllocation)
class SeatAllocationAdmin(admin.ModelAdmin):
    list_display = ('seat_number', 'student', 'seating_plan', 'row', 'column', 'is_present', 'is_locked')
    list_filter = ('seating_plan__room_name', 'is_present', 'is_locked', 'seating_plan__exam__subject')
    search_fields = ('seat_number', 'student__name', 'seating_plan__exam__title')
    ordering = ('seating_plan', 'row', 'column')
    list_select_related = ('seating_plan__exam', 'student')
    list_editable = ('is_present', 'is_locked')


# ═════════════════════════════════════════════════════════════════════════════
# T6 — TEACHER LEAVE MANAGEMENT
# ═════════════════════════════════════════════════════════════════════════════

@admin.register(TeacherLeave)
class TeacherLeaveAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'leave_type', 'start_date', 'end_date', 'status', 'substitute_teacher', 'approved_by')
    list_filter = ('leave_type', 'status', 'teacher', 'start_date')
    search_fields = ('teacher__first_name', 'teacher__last_name', 'reason', 'approval_reason')
    ordering = ('-start_date',)
    date_hierarchy = 'start_date'
    readonly_fields = ('created_at', 'updated_at', 'days_count')
    fieldsets = (
        ('Leave Details', {
            'fields': ('teacher', 'leave_type', 'start_date', 'end_date', 'days_count', 'reason')
        }),
        ('Substitute & Approval', {
            'fields': ('substitute_teacher', 'status', 'approved_by', 'approval_reason', 'approved_at')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    list_select_related = ('teacher', 'substitute_teacher', 'approved_by')


# ── T8  Question Bank ───────────────────────────────────────────────────────────

@admin.register(QuestionBank)
class QuestionBankAdmin(admin.ModelAdmin):
    list_display = ('subject', 'question_type', 'difficulty', 'chapter', 'marks', 'is_active', 'times_used', 'created_at')
    list_filter = ('subject', 'question_type', 'difficulty', 'chapter', 'is_active')
    search_fields = ('question_text', 'chapter', 'tags')
    ordering = ('-created_at',)
    list_per_page = 50
    readonly_fields = ('times_used', 'created_at')


@admin.register(QuestionPaperTemplate)
class QuestionPaperTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'total_marks', 'duration_minutes', 'teacher')
    list_filter = ('subject', 'teacher')
    search_fields = ('name', 'subject__name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)


# ── T9  Reminders & Scheduled Tasks ─────────────────────────────────────────────

@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('title', 'reminder_type', 'teacher', 'student', 'scheduled_for', 'is_sent', 'is_active')
    list_filter = ('reminder_type', 'is_sent', 'is_active', 'scheduled_for')
    search_fields = ('title', 'message', 'teacher__first_name', 'student__name')
    ordering = ('-scheduled_for',)
    autocomplete_fields = ('teacher', 'student', 'subject')
    date_hierarchy = 'scheduled_for'


@admin.register(ScheduledTask)
class ScheduledTaskAdmin(admin.ModelAdmin):
    list_display = ('task_type', 'scheduled_for', 'is_executed', 'executed_at', 'is_active')
    list_filter = ('task_type', 'is_executed', 'is_active', 'scheduled_for')
    search_fields = ('task_type',)
    ordering = ('-scheduled_for',)
    list_per_page = 100
    readonly_fields = ('executed_at',)
    date_hierarchy = 'scheduled_for'


# ═════════════════════════════════════════════════════════════════════════════
#  A3 — INVOICE BILLING / SUBSCRIPTION MODULE
# ═════════════════════════════════════════════════════════════════════════════

class InvoiceInline(admin.TabularInline):
    model = Invoice
    extra = 0
    fields = ('invoice_number', 'amount', 'tax_amount', 'total_amount', 'status', 'issue_date', 'due_date')
    readonly_fields = ('invoice_number', 'total_amount')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('institution', 'plan', 'monthly_price', 'is_active', 'auto_renew', 'started_at', 'expires_at')
    list_filter = ('plan', 'is_active', 'auto_renew')
    search_fields = ('institution',)
    ordering = ('-started_at',)
    inlines = [InvoiceInline]


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'issued_to', 'amount', 'tax_amount', 'total_amount', 'status', 'issue_date', 'paid_date')
    list_filter = ('status', 'issue_date', 'paid_date')
    search_fields = ('invoice_number', 'issued_to')
    ordering = ('-issue_date',)
    readonly_fields = ('invoice_number', 'total_amount')
    date_hierarchy = 'issue_date'
    autocomplete_fields = ('subscription',)
    list_per_page = 50


# ═════════════════════════════════════════════════════════════════════════════
#  A8 — ANALYTICS EXPORT BUNDLE
# ═════════════════════════════════════════════════════════════════════════════
# (admin not needed — export_utils module handles it)


# ═════════════════════════════════════════════════════════════════════════════
#  A9 — CERTIFICATE GENERATOR
# ═════════════════════════════════════════════════════════════════════════════

class CertificateInline(admin.TabularInline):
    model = Certificate
    extra = 0
    fields = ('certificate_number', 'certificate_type', 'issued_date', 'status')
    readonly_fields = ('certificate_number',)


@admin.register(CertificateTemplate)
class CertificateTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('certificate_number', 'student', 'certificate_type', 'status', 'issued_date', 'issued_by')
    list_filter = ('certificate_type', 'status', 'issued_date')
    search_fields = ('certificate_number', 'student__name')
    ordering = ('-created_at',)
    autocomplete_fields = ('student', 'template', 'issued_by')
    readonly_fields = ('certificate_number', 'qr_data_string', 'created_at')
    list_per_page = 50
    date_hierarchy = 'created_at'
    actions = ['mark_issued', 'mark_revoked']

    @admin.action(description='Mark selected certificates as Issued')
    def mark_issued(self, request, queryset):
        queryset.update(status='ISSUED')
        self.message_user(request, 'Selected certificates marked as Issued.')

    @admin.action(description='Revoke selected certificates')
    def mark_revoked(self, request, queryset):
        queryset.update(status='REVOKED')
        self.message_user(request, 'Selected certificates revoked.')


# ═════════════════════════════════════════════════════════════════════════════
#  A14 — API KEY & WEBHOOK SYSTEM
# ═════════════════════════════════════════════════════════════════════════════

class WebhookDeliveryLogInline(admin.TabularInline):
    model = WebhookDeliveryLog
    extra = 0
    fields = ('event_type', 'success', 'response_code', 'attempt', 'delivered_at')
    readonly_fields = ('event_type', 'success', 'response_code', 'attempt', 'delivered_at')
    can_delete = False


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('name', 'key_masked', 'prefix', 'scopes_preview', 'is_active', 'last_used_at', 'expires_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'key', 'prefix')
    ordering = ('-created_at',)
    readonly_fields = ('key', 'created_at', 'last_used_at')

    def key_masked(self, obj):
        if len(obj.key) > 12:
            return obj.key[:8] + '...' + obj.key[-4:]
        return '***'
    key_masked.short_description = 'Key'

    def scopes_preview(self, obj):
        return ', '.join(obj.scopes) if obj.scopes else '-'
    scopes_preview.short_description = 'Scopes'


@admin.register(WebhookEndpoint)
class WebhookEndpointAdmin(admin.ModelAdmin):
    list_display = ('url', 'secret_masked', 'is_active', 'events_preview', 'retry_count', 'last_triggered_at', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('url',)
    ordering = ('-created_at',)
    list_editable = ('is_active',)
    inlines = [WebhookDeliveryLogInline]

    def secret_masked(self, obj):
        if len(obj.secret) > 8:
            return obj.secret[:4] + '...' + obj.secret[-4:]
        return '***'
    secret_masked.short_description = 'Secret'

    def events_preview(self, obj):
        return ', '.join(obj.events) if obj.events else '-'
    events_preview.short_description = 'Events'


@admin.register(WebhookDeliveryLog)
class WebhookDeliveryLogAdmin(admin.ModelAdmin):
    list_display = ('endpoint', 'event_type', 'success', 'response_code', 'attempt', 'delivered_at')
    list_filter = ('success', 'event_type', 'delivered_at')
    search_fields = ('endpoint__url', 'event_type')
    ordering = ('-delivered_at',)
    readonly_fields = ('endpoint', 'event_type', 'payload', 'response_code', 'response_body', 'success', 'attempt')
    list_per_page = 100
    date_hierarchy = 'delivered_at'


# ═════════════════════════════════════════════════════════════════════════════
#  A5 — SUPPORT TICKET SYSTEM
# ═════════════════════════════════════════════════════════════════════════════

class TicketCommentInline(admin.TabularInline):
    model = TicketComment
    extra = 0
    fields = ('author', 'body_short', 'is_internal', 'created_at')
    readonly_fields = ('author', 'body_short', 'created_at')
    can_delete = False

    def body_short(self, obj):
        return (obj.body[:70] + '...') if len(obj.body) > 70 else obj.body
    body_short.short_description = 'Body'


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_id', 'title', 'category', 'priority', 'status', 'reported_by', 'assigned_to', 'created_at')
    list_filter = ('category', 'priority', 'status', 'created_at')
    search_fields = ('ticket_id', 'title', 'description', 'reported_by__username')
    ordering = ('-created_at',)
    list_editable = ('status', 'priority')
    inlines = [TicketCommentInline]
    autocomplete_fields = ('reported_by', 'assigned_to', 'resolved_by')
    date_hierarchy = 'created_at'
    list_per_page = 50


@admin.register(TicketComment)
class TicketCommentAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'author', 'body_short', 'is_internal', 'created_at')
    list_filter = ('is_internal', 'created_at')
    search_fields = ('ticket__ticket_id', 'body', 'author__username')
    ordering = ('-created_at',)
    autocomplete_fields = ('ticket', 'author')

    def body_short(self, obj):
        return (obj.body[:70] + '...') if len(obj.body) > 70 else obj.body
    body_short.short_description = 'Comment'


# ═════════════════════════════════════════════════════════════════════════════
#  A10 — SSO PROVIDER
# ═════════════════════════════════════════════════════════════════════════════

@admin.register(SSOProvider)
class SSOProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'provider_type', 'is_active', 'created_at')
    list_filter = ('provider_type', 'is_active', 'created_at')
    search_fields = ('name', 'client_id')
    ordering = ('name',)
    list_editable = ('is_active',)
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {'fields': ('name', 'provider_type', 'is_active')}),
        ('Credentials', {'fields': ('client_id', 'client_secret')}),
    )


