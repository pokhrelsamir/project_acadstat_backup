from django import forms
from datetime import date as _date
from core.models import Result, TERMINAL_CHOICES
from .models import (
    GradeScale, TeacherEvaluation, Message, StudentNote, MLPrediction, Announcement,
    Subscription, Invoice, Certificate, CertificateTemplate, SupportTicket, SystemConfig,
    LicenseKey, UserRole, UserProfile, ResultPublishSession,
    ParentUser, LessonPlan, SyllabusCoverage,
    GradingRubric, RubricCriterion, ExamSeatingPlan,
    QuestionBank, QuestionPaperTemplate, Reminder,
    Student, Subject,
)
from django.contrib.auth.decorators import login_required

def get_total_marks_initial(request):
    return 100

class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['student', 'subject', 'terminal', 'marks_obtained', 'total_marks']
        widgets = {
            'student': forms.Select(attrs={
                'class': 'form-control',
                'style': 'padding: 12px; border: 2px solid #e0d4f7; border-radius: 8px; font-size: 1rem;'
            }),
            'subject': forms.Select(attrs={
                'class': 'form-control',
                'style': 'padding: 12px; border: 2px solid #e0d4f7; border-radius: 8px; font-size: 1rem;'
            }),
            'terminal': forms.Select(attrs={
                'class': 'form-control',
                'style': 'padding: 12px; border: 2px solid #e0d4f7; border-radius: 8px; font-size: 1rem;',
            }),
            'marks_obtained': forms.NumberInput(attrs={
                'class': 'form-control',
                'style': 'padding: 12px; border: 2px solid #e0d4f7; border-radius: 8px; font-size: 1rem;',
                'placeholder': 'Enter marks obtained',
                'step': '0.01'
            }),
            'total_marks': forms.NumberInput(attrs={
                'class': 'form-control',
                'style': 'padding: 12px; border: 2px solid #e0d4f7; border-radius: 8px; font-size: 1rem;',
                'step': '0.01'
            }),
        }

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['terminal'].choices = TERMINAL_CHOICES
        if request and hasattr(request, 'teacher') and request.teacher:
            self.fields['total_marks'].disabled = True
            self.fields['total_marks'].widget.attrs['readonly'] = True
            self.fields['total_marks'].widget.attrs['style'] = (
                'padding: 12px; border: 2px solid #e0d4f7; border-radius: 8px; '
                'font-size: 1rem; background-color: #f5f5f5; cursor: not-allowed;'
            )


class GradeScaleForm(forms.ModelForm):
    class Meta:
        model = GradeScale
        fields = ['name', 'pass_mark_percent', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'pass_mark_percent': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class TeacherEvaluationForm(forms.ModelForm):
    class Meta:
        model = TeacherEvaluation
        fields = ['subject_performance', 'punctuality', 'communication', 'student_satisfaction', 'comments']
        widgets = {
            'subject_performance': forms.NumberInput(attrs={
                'class': 'form-control', 'type': 'range', 'min': 1, 'max': 100,
                'style': 'width: 100%;',
                'oninput': "this.nextElementSibling.textContent = this.value",
            }),
            'punctuality': forms.NumberInput(attrs={
                'class': 'form-control', 'type': 'range', 'min': 1, 'max': 100,
                'style': 'width: 100%;',
                'oninput': "this.nextElementSibling.textContent = this.value",
            }),
            'communication': forms.NumberInput(attrs={
                'class': 'form-control', 'type': 'range', 'min': 1, 'max': 100,
                'style': 'width: 100%;',
                'oninput': "this.nextElementSibling.textContent = this.value",
            }),
            'student_satisfaction': forms.NumberInput(attrs={
                'class': 'form-control', 'type': 'range', 'min': 1, 'max': 100,
                'style': 'width: 100%;',
                'oninput': "this.nextElementSibling.textContent = this.value",
            }),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Optional comments...'}),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['recipient_student', 'subject', 'user']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject (optional)',
            }),
            'user': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Type your message here...',
            }),
            'recipient_student': forms.Select(attrs={
                'class': 'form-control',
            }),
        }


class StudentNoteForm(forms.ModelForm):
    class Meta:
        model = StudentNote
        fields = ['title', 'content', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Note title',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter your note...',
            }),
            'priority': forms.Select(attrs={
                'class': 'form-control',
            }),
        }


class MLPredictionForm(forms.ModelForm):
    class Meta:
        model = MLPrediction
        fields = ['student', 'subject', 'predicted_grade', 'confidence_score']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'predicted_grade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'A+ / B / C...'}),
            'confidence_score': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100, 'step': '0.1'}),
        }


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'audience', 'target_class', 'priority', 'attachment']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Announcement title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Write the announcement...'}),
            'audience': forms.Select(attrs={'class': 'form-control'}),
            'target_class': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'If audience=class, enter class'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'attachment': forms.FileInput(attrs={'class': 'form-control'}),
        }


# ═════════════════════════════════════════════════════════════════════════════
# A2 — LICENSE KEY SYSTEM FORMS
# ═════════════════════════════════════════════════════════════════════════════
# ═════════════════════════════════════════════════════════════════════════════

class LicenseKeyForm(forms.ModelForm):
    class Meta:
        model = LicenseKey
        fields = ['institution_name', 'max_teachers', 'max_students', 'max_branches', 'expires_at', 'notes']
        widgets = {
            'institution_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Institution name'}),
            'max_teachers': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'max_students': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'max_branches': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'expires_at': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional notes...'}),
        }


# ═════════════════════════════════════════════════════════════════════════════
# A6 — RBAC ROLE & PERMISSION FORMS
# ═════════════════════════════════════════════════════════════════════════════

class UserRoleForm(forms.ModelForm):
    permissions = forms.MultipleChoiceField(
        choices=[
            ('can_manage_students', 'Manage Students'),
            ('can_manage_teachers', 'Manage Teachers'),
            ('can_manage_subjects', 'Manage Subjects'),
            ('can_manage_fees', 'Manage Fees'),
            ('can_manage_exams', 'Manage Exams'),
            ('can_manage_attendance', 'Manage Attendance'),
            ('can_manage_materials', 'Manage Materials'),
            ('can_view_reports', 'View Reports'),
            ('can_manage_system', 'Manage System'),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = UserRole
        fields = ['name', 'code', 'description', 'is_system_role', 'permissions']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_system_role': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            selected = [k for k, v in [
                ('can_manage_students', self.instance.can_manage_students),
                ('can_manage_teachers', self.instance.can_manage_teachers),
                ('can_manage_subjects', self.instance.can_manage_subjects),
                ('can_manage_fees', self.instance.can_manage_fees),
                ('can_manage_exams', self.instance.can_manage_exams),
                ('can_manage_attendance', self.instance.can_manage_attendance),
                ('can_manage_materials', self.instance.can_manage_materials),
                ('can_view_reports', self.instance.can_view_reports),
                ('can_manage_system', self.instance.can_manage_system),
            ] if v]
            self.initial['permissions'] = selected

    def save(self, commit=True):
        instance = super().save(commit=False)
        selected_perms = self.cleaned_data.get('permissions', [])
        perm_map = {
            'can_manage_students': 'can_manage_students',
            'can_manage_teachers': 'can_manage_teachers',
            'can_manage_subjects': 'can_manage_subjects',
            'can_manage_fees': 'can_manage_fees',
            'can_manage_exams': 'can_manage_exams',
            'can_manage_attendance': 'can_manage_attendance',
            'can_manage_materials': 'can_manage_materials',
            'can_view_reports': 'can_view_reports',
            'can_manage_system': 'can_manage_system',
        }
        for perm_key, field_name in perm_map.items():
            setattr(instance, field_name, perm_key in selected_perms)
        if commit:
            instance.save()
        return instance


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user', 'role']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
        }


# ═════════════════════════════════════════════════════════════════════════════
# A13 — RESULT PUBLISH SESSION FORMS
# ═════════════════════════════════════════════════════════════════════════════

class ResultPublishSessionForm(forms.ModelForm):
    class Meta:
        model = ResultPublishSession
        fields = ['name', 'subject', 'target_class', 'academic_year', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 1st Terminal 2025'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'target_class': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 10, XI, S1'}),
            'academic_year': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class ResultSessionRemarkForm(forms.Form):
    remarks = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Add remark...'}),
        required=False,
    )


# ═════════════════════════════════════════════════════════════════════════════
# A11 — PARENT USER FORMS
# ═════════════════════════════════════════════════════════════════════════════

class ParentUserForm(forms.ModelForm):
    class Meta:
        model = ParentUser
        fields = ['user', 'parent', 'phone', 'is_verified']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'parent': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1-555-0123'}),
            'is_verified': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }



# ═════════════════════════════════════════════════════════════════════════════
# T2 — LESSON PLAN FORMS
# ═════════════════════════════════════════════════════════════════════════════

class LessonPlanForm(forms.ModelForm):
    class Meta:
        model = LessonPlan
        fields = ['subject', 'title', 'description', 'class_section', 'chapter_topic',
                  'planned_date', 'duration_minutes', 'teaching_method',
                  'learning_outcomes', 'resources_used', 'status', 'remarks']
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lesson title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'class_section': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 10A, XI-B'}),
            'chapter_topic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Chapter / Topic name'}),
            'planned_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'teaching_method': forms.Select(attrs={'class': 'form-control'}),
            'learning_outcomes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'What will students learn?'}),
            'resources_used': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class SyllabusCoverageForm(forms.ModelForm):
    class Meta:
        model = SyllabusCoverage
        fields = ['subject', 'class_section', 'chapter_name', 'estimated_hours',
                  'actual_hours', 'planned_order', 'is_completed', 'notes']
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'class_section': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 10A'}),
            'chapter_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Chapter / Topic name'}),
            'estimated_hours': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'actual_hours': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'planned_order': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'is_completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


# ═════════════════════════════════════════════════════════════════════════════
# T3 — RUBRIC FORMS
# ═════════════════════════════════════════════════════════════════════════════

class GradingRubricForm(forms.ModelForm):
    class Meta:
        model = GradingRubric
        fields = ['name', 'subject', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rubric name'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class RubricCriterionForm(forms.ModelForm):
    class Meta:
        model = RubricCriterion
        fields = ['name', 'max_score', 'weight_percent', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Accuracy'}),
            'max_score': forms.NumberInput(attrs={'class': 'form-control', 'min': 0.1, 'step': '0.1'}),
            'weight_percent': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100, 'step': '0.1'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }


# ═════════════════════════════════════════════════════════════════════════════
# T5 — SEATING PLAN FORMS
# ═════════════════════════════════════════════════════════════════════════════

class ExamSeatingPlanForm(forms.ModelForm):
    class Meta:
        model = ExamSeatingPlan
        fields = ['exam', 'room_name', 'room_capacity', 'arrangement_type', 'notes']
        widgets = {
            'exam': forms.Select(attrs={'class': 'form-control'}),
            'room_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Hall 1, Room A'}),
            'room_capacity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'arrangement_type': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


# ── T8 Question Bank forms ───────────────────────────────────────────────────────

class QuestionBankForm(forms.ModelForm):
    class Meta:
        from core.models import QuestionBank
        model = QuestionBank
        fields = ['subject', 'question_text', 'question_type', 'options', 'correct_answer',
                  'difficulty', 'chapter', 'marks', 'tags']
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'question_text': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3, 'placeholder': 'Enter question text...'
            }),
            'question_type': forms.Select(attrs={'class': 'form-control'}),
            'options': forms.HiddenInput(),
            'correct_answer': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'e.g. A or Paris or True'
            }),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
            'chapter': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'e.g. Chapter 1: Atoms'
            }),
            'marks': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'value': 1}),
            'tags': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Comma-separated tags'
            }),
        }


class QuestionPaperTemplateForm(forms.ModelForm):
    class Meta:
        from core.models import QuestionPaperTemplate
        model = QuestionPaperTemplate
        fields = ['name', 'subject', 'total_marks', 'duration_minutes', 'distribution', 'chapters']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Test 1, Mid-Sem, Final...'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'total_marks': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'distribution': forms.HiddenInput(),
            'chapters': forms.HiddenInput(),
        }


# ── T9 Reminder form ─────────────────────────────────────────────────────────────

class ReminderForm(forms.ModelForm):
    class Meta:
        from core.models import Reminder
        model = Reminder
        fields = ['reminder_type', 'student', 'subject', 'title', 'message',
                  'scheduled_for', 'recurrence', 'recurrence_until']
        widgets = {
            'reminder_type': forms.Select(attrs={'class': 'form-control'}),
            'student': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Reminder title'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Reminder message...'}),
            'scheduled_for': forms.DateTimeInput(attrs={
                'class': 'form-control', 'type': 'datetime-local'
            }),
            'recurrence': forms.Select(attrs={'class': 'form-control'}),
            'recurrence_until': forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date'
            }),
        }


# ═════════════════════════════════════════════════════════════════════════════
# A3 — INVOICE / SUBSCRIPTION FORMS
# ═════════════════════════════════════════════════════════════════════════════

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['institution', 'plan', 'monthly_price', 'is_active', 'auto_renew', 'expires_at']
        widgets = {
            'institution': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Institution name'}),
            'plan': forms.Select(attrs={'class': 'form-control'}),
            'monthly_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'expires_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'auto_renew': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['invoice_number', 'subscription', 'issued_to', 'amount', 'tax_amount',
                  'issue_date', 'due_date', 'status', 'line_items', 'payment_link']
        widgets = {
            'invoice_number': forms.TextInput(attrs={'class': 'form-control'}),
            'subscription': forms.Select(attrs={'class': 'form-control'}),
            'issued_to': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bill to'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'tax_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'issue_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'payment_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'line_items': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 5,
                'placeholder': '[{"description":"Tuition Fee","qty":1,"unit_price":500,"total":500}]'
            }),
        }


class InvoiceQuickCreateForm(forms.Form):
    """Quick invoice creation with dynamic line items."""
    subscription = forms.ChoiceField(
        choices=[('', '— No subscription —')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
    )
    issued_to = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bill to'}),
    )
    amount = forms.DecimalField(
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
    )
    tax_amount = forms.DecimalField(
        max_digits=10, decimal_places=2, required=False, initial=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
    )
    issue_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        initial=_date.today,
    )
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
    )
    line_items = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control', 'rows': 4,
            'placeholder': '[{"description":"Tuition Fee","qty":1,"unit_price":500,"total":500}]'
        }),
        initial='[]',
    )


# ═════════════════════════════════════════════════════════════════════════════
# A9 — CERTIFICATE FORMS
# ═════════════════════════════════════════════════════════════════════════════

class CertificateTemplateForm(forms.ModelForm):
    class Meta:
        model = CertificateTemplate
        fields = ['name', 'html_content', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'html_content': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 15,
                'style': 'font-family:monospace;font-size:.85rem;'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class CertificateGenerateForm(forms.Form):
    CERT_TYPES = [
        ('M', 'Mark Certificate'),
        ('TC', 'Transfer Certificate'),
        ('BON', 'Bonafide Certificate'),
        ('TR', 'Transfer'),
        ('ACH', 'Achievement'),
    ]
    student = forms.ModelChoiceField(
        queryset=Student.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    certificate_type = forms.ChoiceField(
        choices=CERT_TYPES,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    terminal = forms.CharField(
        max_length=10, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 1st, 2nd, Final'}),
    )
    academic_year = forms.CharField(
        max_length=20, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2025-2026'}),
    )


# ═════════════════════════════════════════════════════════════════════════════
# A5 — SUPPORT TICKET FORMS
# ═════════════════════════════════════════════════════════════════════════════

class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ['title', 'description', 'category', 'priority', 'screenshot']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brief title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Describe the issue...'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'screenshot': forms.FileInput(attrs={'class': 'form-control'}),
        }


class TicketCommentForm(forms.Form):
    body = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write a comment...'}),
    )
    is_internal = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )
