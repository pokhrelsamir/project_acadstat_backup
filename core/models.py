from django.db import models
from django.contrib.auth.models import User
import uuid

# Helper always-available
from django.db.models import Q
from decimal import Decimal

# ─────────────────────────────────────────────────────────────────────────────
# 1. SUBJECT MODEL
# ─────────────────────────────────────────────────────────────────────────────
class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    total_marks = models.PositiveIntegerField(default=100, help_text="Default total marks for this subject")
    is_practical = models.BooleanField(default=False, help_text="Is this a practical/internal subject")
    pass_marks = models.PositiveIntegerField(default=40, help_text="Minimum marks to pass")

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

# ─────────────────────────────────────────────────────────────────────────────
# 2. EDUCATION LEVEL MODEL
# ─────────────────────────────────────────────────────────────────────────────
class EducationLevel(models.Model):
    SCHOOL = 'school'
    COLLEGE = 'college'
    BACHELOR = 'bachelor'
    LEVEL_CHOICES = [
        (SCHOOL, 'School Level (1-10)'),
        (COLLEGE, 'College Level (XI-XII)'),
        (BACHELOR, 'Bachelor Level'),
    ]
    code = models.CharField(max_length=20, primary_key=True, choices=LEVEL_CHOICES)
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['code']

    def __str__(self):
        return self.name

    @property
    def display_name(self):
        return dict(self.LEVEL_CHOICES).get(self.code, self.name)

# ─────────────────────────────────────────────────────────────────────────────
# 3. SEMESTER MODEL
# ─────────────────────────────────────────────────────────────────────────────
class Semester(models.Model):
    SEMESTER_CHOICES = [(i, f'Semester {i}') for i in range(1, 9)]
    number = models.PositiveSmallIntegerField(primary_key=True, choices=SEMESTER_CHOICES)
    label = models.CharField(max_length=20, default='')

    class Meta:
        ordering = ['number']

    def __str__(self):
        return f'Semester {self.number}'

# ─────────────────────────────────────────────────────────────────────────────
# 4. ACADEMIC YEAR MODEL
# ─────────────────────────────────────────────────────────────────────────────
class AcademicYear(models.Model):
    name = models.CharField(max_length=20, unique=True, help_text="e.g. 2025-2026")
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.is_current:
            AcademicYear.objects.exclude(id=self.id).update(is_current=False)
        super().save(*args, **kwargs)

# ─────────────────────────────────────────────────────────────────────────────
# 5. DEPARTMENT MODEL
# ─────────────────────────────────────────────────────────────────────────────
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    head = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True, blank=True, related_name='headed_departments')
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

# ─────────────────────────────────────────────────────────────────────────────
# 6. GRADE SCALE MODEL
# ─────────────────────────────────────────────────────────────────────────────
class GradeScale(models.Model):
    name = models.CharField(max_length=50, unique=True, help_text="e.g. Standard, Division, GPA 4.0")
    pass_mark_percent = models.FloatField(default=40.0, help_text="Minimum % to pass")
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_grade(self, percentage):
        pct = float(percentage)
        if pct >= 90:
            return 'A+'
        elif pct >= 80:
            return 'A'
        elif pct >= 70:
            return 'B+'
        elif pct >= 60:
            return 'B'
        elif pct >= 50:
            return 'C+'
        elif pct >= 40:
            return 'C'
        elif pct >= 30:
            return 'D'
        return 'F'

    def get_grade_point(self, percentage):
        pct = float(percentage)
        if pct >= 90:
            return 4.0
        elif pct >= 80:
            return 3.6
        elif pct >= 70:
            return 3.2
        elif pct >= 60:
            return 2.8
        elif pct >= 50:
            return 2.4
        elif pct >= 40:
            return 2.0
        elif pct >= 30:
            return 1.6
        return 0.0

    @property
    def grade_labels(self):
        return ['A+', 'A', 'B+', 'B', 'C+', 'C', 'D', 'F']

# ─────────────────────────────────────────────────────────────────────────────
# 7. TEACHER MODEL
# ─────────────────────────────────────────────────────────────────────────────
class Teacher(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='teacher_profile')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    subjects = models.ManyToManyField(Subject, related_name='teachers', blank=True)
    levels = models.ManyToManyField(EducationLevel, related_name='teachers', blank=True)
    semesters = models.ManyToManyField(Semester, related_name='teachers', blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='teachers')
    email = models.EmailField(unique=True, null=True, blank=True)
    joining_date = models.DateField(auto_now_add=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False, help_text="Designates if this teacher has admin privileges")
    role = models.ForeignKey('UserRole', null=True, blank=True, on_delete=models.SET_NULL, help_text="RBAC role (optional, legacy is_admin kept for compatibility)")

    class Meta:
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        name = f"{self.first_name} {self.last_name}"
        try:
            if self.levels.filter(code__in=['college', 'bachelor']).exists():
                return f"Prof. {name}"
        except Exception:
            pass
        return name

    def can_access_subject(self, subject):
        return self.subjects.filter(id=subject.id).exists()

    def can_access_student(self, student):
        return student.teacher == self

    def get_workload_summary(self):
        subjects = self.subjects.count()
        students = self.students.count()
        assigned_classes = Student.objects.filter(teacher=self).values('student_class').distinct().count()
        return {
            'subjects': subjects,
            'total_students': students,
            'assigned_classes': assigned_classes,
        }

# ─────────────────────────────────────────────────────────────────────────────
# 8. PARENT MODEL
# ─────────────────────────────────────────────────────────────────────────────
class Parent(models.Model):
    student = models.OneToOneField('Student', on_delete=models.CASCADE, related_name='parent_info')
    father_name = models.CharField(max_length=100, blank=True)
    mother_name = models.CharField(max_length=100, blank=True)
    guardian_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    relation = models.CharField(max_length=50, default='Father', help_text="Relationship to student")
    is_primary_contact = models.BooleanField(default=True)

    class Meta:
        ordering = ['student__name']

    def __str__(self):
        return f"Parent of {self.student.name} – {self.guardian_name or self.father_name or 'N/A'}"

# ─────────────────────────────────────────────────────────────────────────────
# 9. STUDENT MODEL (extended)
# ─────────────────────────────────────────────────────────────────────────────
class Student(models.Model):
    LEVEL_CHOICES = [
        ('school', 'School Level (1-10)'),
        ('college', 'College Level (XI-XII)'),
        ('bachelor', 'Bachelor Level'),
    ]

    LEVEL_SCHOOL = 'school'
    LEVEL_COLLEGE = 'college'
    LEVEL_BACHELOR = 'bachelor'

    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='school')
    student_class = models.CharField(max_length=20, help_text="Class/Division (e.g., 1, 5, 10, XI, XII, etc.)")
    section = models.CharField(max_length=5)
    semester = models.CharField(max_length=20, null=True, blank=True, help_text="Semester for Bachelor level (1-8)")
    date_of_birth = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='student_images/', null=True, blank=True, help_text="Student photo")
    created_at = models.DateTimeField(auto_now_add=True)
    teachers = models.ManyToManyField(Teacher, related_name='students', blank=True)

    # Contact / Personal
    email = models.EmailField(null=True, blank=True, help_text="Student email for notifications")
    phone = models.CharField(max_length=20, null=True, blank=True, help_text="Student phone number")

    # Extended
    blood_group = models.CharField(max_length=10, blank=True, help_text="e.g. A+, B-, O+")
    gender = models.CharField(max_length=10, choices=[('M','Male'),('F','Female'),('O','Other')], blank=True)
    admission_date = models.DateField(null=True, blank=True, help_text="Date of admission")
    is_promoted = models.BooleanField(default=False, help_text="Has the student been promoted to next class")
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='students')
    house = models.CharField(max_length=50, blank=True, help_text="e.g. Red, Blue, Green, Yellow House")
    scholarship = models.BooleanField(default=False, help_text="Is the student on scholarship")
    emergency_contact = models.CharField(max_length=15, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.roll_number})"

    @property
    def current_age(self):
        from datetime import date
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None

    @property
    def current_class_level(self):
        return f"{self.student_class} {self.section}" if self.section else self.student_class

    @property
    def attendance_percentage(self):
        total = self.attendance_records.count()
        if total == 0:
            return 0
        present = self.attendance_records.filter(status='present').count()
        return round((present / total) * 100, 1)

    @property
    def cgpa(self):
        results = self.result_set.all()
        if not results.exists():
            return 0.0
        gs = GradeScale.objects.filter(is_active=True).first()
        if not gs:
            return 0.0
        total = 0.0
        count = 0
        for r in results:
            pct = (r.marks_obtained / r.total_marks * 100) if r.total_marks > 0 else 0
            total += gs.get_grade_point(pct)
            count += 1
        return round(total / count, 2) if count > 0 else 0.0

    @property
    def overall_grade(self):
        results = self.result_set.all()
        if not results.exists():
            return '-'
        gs = GradeScale.objects.filter(is_active=True).first()
        if not gs:
            return '-'
        total = pct_list = 0.0
        for r in results:
            pct = (r.marks_obtained / r.total_marks * 100) if r.total_marks > 0 else 0
            pct_list += 1
            total += pct
        avg = total / pct_list if pct_list else 0
        return gs.get_grade(avg)

    @property
    def rank_in_class(self):
        from django.db.models import Sum, F, FloatField, ExpressionWrapper
        students = Student.objects.filter(
            level=self.level,
            student_class=self.student_class
        ).exclude(id=self.id)

        student_scores = []
        for s in students:
            results = s.result_set.all()
            if results.exists():
                total_obt = sum(r.marks_obtained for r in results)
                total_pos = sum(r.total_marks for r in results)
                pct = (total_obt / total_pos * 100) if total_pos > 0 else 0
                student_scores.append((s.id, pct))

        self_scores = self.result_set.all()
        if self_scores.exists():
            total_obt = sum(r.marks_obtained for r in self_scores)
            total_pos = sum(r.total_marks for r in self_scores)
            self_pct = (total_obt / total_pos * 100) if total_pos > 0 else 0
        else:
            self_pct = 0

        student_scores.append((self.id, self_pct))
        student_scores.sort(key=lambda x: x[1], reverse=True)
        for rank, (sid, _) in enumerate(student_scores, 1):
            if sid == self.id:
                return rank
        return len(student_scores) + 1

    def lock_grade_sheet(self, teacher=None, reason=''):
        for result in self.result_set.all():
            ResultLock.objects.get_or_create(
                result=result,
                defaults={'locked_by': teacher, 'reason': reason}
            )

    @property
    def grade_sheet_locked(self):
        return ResultLock.objects.filter(result__student=self).exists()

# ─────────────────────────────────────────────────────────────────────────────
# 10. STUDENT ACADEMIC HISTORY
# ─────────────────────────────────────────────────────────────────────────────
class StudentAcademicHistory(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='history')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.SET_NULL, null=True)
    previous_class = models.CharField(max_length=20)
    previous_section = models.CharField(max_length=5, blank=True)
    promoted_to_class = models.CharField(max_length=20)
    promoted_to_section = models.CharField(max_length=5, blank=True)
    total_marks_obtained = models.FloatField(default=0)
    total_marks = models.FloatField(default=0)
    percentage = models.FloatField(default=0)
    grade = models.CharField(max_length=10, blank=True)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-academic_year__start_date']
        verbose_name_plural = 'Student Academic Histories'

    def __str__(self):
        return f"{self.student.name} — {self.academic_year or 'Unknown Year'} → {self.promoted_to_class}"

    def save(self, *args, **kwargs):
        if self.total_marks > 0:
            self.percentage = round((self.total_marks_obtained / self.total_marks) * 100, 2)
        if self.percentage:
            gs = GradeScale.objects.filter(is_active=True).first()
            if gs:
                self.grade = gs.get_grade(self.percentage)
        super().save(*args, **kwargs)

# ─────────────────────────────────────────────────────────────────────────────
# 11. ATTENDANCE MODEL
# ─────────────────────────────────────────────────────────────────────────────
class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    remarks = models.CharField(max_length=200, blank=True)
    recorded_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['student', 'subject', 'date']
        ordering = ['-date', 'student__name']
        indexes = [
            models.Index(fields=['student', 'date']),
            models.Index(fields=['date', 'status']),
        ]

    def __str__(self):
        return f"{self.student.name} — {self.date} — {self.get_status_display()}"

# ─────────────────────────────────────────────────────────────────────────────
# 12. ASSIGNMENT MODEL
# ─────────────────────────────────────────────────────────────────────────────
class Assignment(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='assignments')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='assigned_homeworks')
    target_class = models.CharField(max_length=20, help_text="Target class (e.g., 10, XI, S1)")
    target_section = models.CharField(max_length=5, default='', help_text="Target section")
    target_students = models.ManyToManyField(Student, blank=True, related_name='assigned_assignments', help_text="Leave empty for whole class")
    file = models.FileField(upload_to='assignments/', null=True, blank=True)
    file_url = models.URLField(blank=True, null=True)
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    total_marks = models.PositiveIntegerField(default=10)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-due_date']

    def __str__(self):
        return f"{self.title} — {self.subject.name} (Due: {self.due_date.strftime('%b %d')})"

    @property
    def is_overdue(self):
        from django.utils import timezone
        return not self.is_published or timezone.now() > self.due_date

    @property
    def submissions_count(self):
        return self.submissions.count()

    @property
    def pending_count(self):
        from django.utils import timezone
        enrolled = Student.objects.filter(student_class=self.target_class)
        if self.target_students.exists():
            enrolled = self.target_students.all()
        total_enrolled = enrolled.count()
        submitted = self.submissions.count()
        return max(total_enrolled - submitted, 0)

# ─────────────────────────────────────────────────────────────────────────────
# 13. ASSIGNMENT SUBMISSION MODEL
# ─────────────────────────────────────────────────────────────────────────────
class AssignmentSubmission(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('graded', 'Graded'),
        ('late', 'Late'),
        ('missing', 'Missing'),
    ]
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='assignment_submissions')
    file = models.FileField(upload_to='assignment_submissions/', null=True, blank=True)
    file_url = models.URLField(blank=True, null=True)
    text_answer = models.TextField(blank=True, help_text="Written response")
    marks_obtained = models.FloatField(null=True, blank=True)
    teacher_feedback = models.TextField(blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='submitted')
    submitted_at = models.DateTimeField(auto_now_add=True)
    graded_at = models.DateTimeField(null=True, blank=True)
    graded_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='graded_submissions')

    class Meta:
        unique_together = ['assignment', 'student']
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.student.name} – {self.assignment.title} ({self.status})"

    @property
    def score_percentage(self):
        if self.marks_obtained is not None and self.assignment.total_marks > 0:
            return round((self.marks_obtained / self.assignment.total_marks) * 100, 1)
        return None

    @property
    def is_late(self):
        from django.utils import timezone
        return self.submitted_at > self.assignment.due_date

# ─────────────────────────────────────────────────────────────────────────────
# 14. EXAM MODEL
# ─────────────────────────────────────────────────────────────────────────────
class Exam(models.Model):
    EXAM_TYPE_CHOICES = [
        ('unit', 'Unit Test'),
        ('mid', 'Mid Term'),
        ('terminal', 'Terminal Exam'),
        ('final', 'Final Exam'),
        ('prelim', 'Preliminary'),
        ('practical', 'Practical / Viva'),
    ]
    title = models.CharField(max_length=200, help_text="e.g. Mid Term 2025")
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPE_CHOICES, default='terminal')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exams')
    target_class = models.CharField(max_length=20)
    target_section = models.CharField(max_length=5, default='')
    exam_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    total_marks = models.PositiveIntegerField(default=100)
    passing_marks = models.PositiveIntegerField(default=40)
    venue = models.CharField(max_length=200, blank=True, help_text="Room / Hall / Online")
    instructions = models.TextField(blank=True)
    is_published = models.BooleanField(default=False)
    published_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='published_exams')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['exam_date', 'start_time']

    def __str__(self):
        return f"{self.title} — {self.subject.name} ({self.target_class})"

# ─────────────────────────────────────────────────────────────────────────────
# 15. FEE MODEL
# ─────────────────────────────────────────────────────────────────────────────
class Fee(models.Model):
    STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('overdue', 'Overdue'),
        ('waived', 'Waived'),
    ]
    FEE_TYPE_CHOICES = [
        ('tuition', 'Tuition Fee'),
        ('exam', 'Exam Fee'),
        ('library', 'Library Fee'),
        ('transport', 'Transport Fee'),
        ('laboratory', 'Laboratory Fee'),
        ('sports', 'Sports Fee'),
        ('misc', 'Miscellaneous'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fees')
    fee_type = models.CharField(max_length=30, choices=FEE_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    paid_date = models.DateField(null=True, blank=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    receipt_number = models.CharField(max_length=50, blank=True, unique=True)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_fees')

    class Meta:
        ordering = ['-due_date', 'student__name']

    def __str__(self):
        return f"{self.student.name} — {self.get_fee_type_display()} — {self.status}"

    @property
    def balance(self):
        return float(self.amount) - float(self.amount_paid)

    def save(self, *args, **kwargs):
        if self.amount_paid >= float(self.amount):
            self.status = 'paid'
        elif self.paid_date and self.amount_paid > 0:
            self.status = 'paid'
        super().save(*args, **kwargs)

# ─────────────────────────────────────────────────────────────────────────────
# 16. ANNOUNCEMENT MODEL
# ─────────────────────────────────────────────────────────────────────────────
class Announcement(models.Model):
    AUDIENCE_CHOICES = [
        ('all', 'All (Students, Teachers, Admin)'),
        ('students', 'Students Only'),
        ('teachers', 'Teachers Only'),
        ('class', 'Specific Class'),
        ('parents', 'Parents'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    title = models.CharField(max_length=200)
    content = models.TextField()
    audience = models.CharField(max_length=20, choices=AUDIENCE_CHOICES, default='all')
    target_class = models.CharField(max_length=20, blank=True, help_text="If audience=class, specify class (e.g., 10, XI)")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    attachment = models.FileField(upload_to='announcements/', null=True, blank=True)
    published_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='announcements')
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True, help_text="After this date the announcement auto-hides")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return f"[{self.get_priority_display()}] {self.title}"

# ─────────────────────────────────────────────────────────────────────────────
# 17. ACTIVITY LOG MODEL
# ─────────────────────────────────────────────────────────────────────────────
class ActivityLog(models.Model):
    ACTION_CHOICES = [
        ('login', 'User Login'),
        ('logout', 'User Logout'),
        ('add_marks', 'Added Marks'),
        ('edit_marks', 'Edited Marks'),
        ('delete_marks', 'Deleted Marks'),
        ('add_student', 'Added Student'),
        ('edit_student', 'Edited Student'),
        ('delete_student', 'Deleted Student'),
        ('add_teacher', 'Added Teacher'),
        ('add_material', 'Uploaded Course Material'),
        ('delete_material', 'Deleted Course Material'),
        ('publish_result', 'Published Results'),
        ('add_assignment', 'Created Assignment'),
        ('add_attendance', 'Recorded Attendance'),
        ('add_exam', 'Created Exam'),
        ('add_fee', 'Created Fee Record'),
        ('add_announcement', 'Published Announcement'),
        ('bulk_upload', 'Bulk Marks Upload'),
        ('promote_student', 'Promoted Student'),
        ('other', 'Other'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs', null=True, blank=True)
    action = models.CharField(max_length=30, choices=ACTION_CHOICES)
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'action', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.user} – {self.get_action_display()} @ {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

# ─────────────────────────────────────────────────────────────────────────────
# 18. TEACHER EVALUATION MODEL
# ─────────────────────────────────────────────────────────────────────────────
class TeacherEvaluation(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='evaluations')
    evaluator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='evaluations_given')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.SET_NULL, null=True)
    subject_performance = models.PositiveIntegerField(default=80, help_text="Subject knowledge rating (1-100)")
    punctuality = models.PositiveIntegerField(default=80, help_text="Punctuality rating (1-100)")
    communication = models.PositiveIntegerField(default=80, help_text="Communication skills (1-100)")
    student_satisfaction = models.PositiveIntegerField(default=80, help_text="Student satisfaction (1-100)")
    overall_score = models.FloatField(default=0.0, help_text="Auto-calculated average")
    comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['teacher', 'evaluator', 'academic_year']

    def __str__(self):
        return f"Eval: {self.teacher.get_full_name()} by {self.evaluator}"

    def save(self, *args, **kwargs):
        self.overall_score = round(
            (self.subject_performance + self.punctuality + self.communication + self.student_satisfaction) / 4, 1
        )
        super().save(*args, **kwargs)

# ─────────────────────────────────────────────────────────────────────────────
# 19. NOTIFICATION MODEL
# ─────────────────────────────────────────────────────────────────────────────
class Notification(models.Model):
    TYPE_CHOICES = [
        ('info', 'Information'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('danger', 'Danger'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    recipient = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='info')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    link_url = models.URLField(blank=True, null=True)
    sender = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_notifications')
    material = models.ForeignKey('CourseMaterial', on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} – {self.recipient.name if self.recipient else 'Bulk'}"

# ─────────────────────────────────────────────────────────────────────────────
# 20. COURSE MATERIALS MODEL
# ─────────────────────────────────────────────────────────────────────────────
class CourseMaterial(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='materials')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='uploaded_materials')
    file = models.FileField(upload_to='course_materials/', blank=True, null=True)
    file_url = models.URLField(blank=True, null=True, help_text="External link to material")
    upload_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-upload_date']

    def __str__(self):
        return f"{self.title} – {self.subject.name}"

    def get_file_name(self):
        if self.file:
            return self.file.name.split('/')[-1]
        return None

# ─────────────────────────────────────────────────────────────────────────────
# 21. RESULT MODEL
# ─────────────────────────────────────────────────────────────────────────────
TERMINAL_CHOICES = [
    ('1st', '1st Terminal'),
    ('2nd', '2nd Terminal'),
    ('3rd', '3rd Terminal'),
    ('Final', 'Final Terminal'),
]

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    terminal = models.CharField(max_length=10, choices=TERMINAL_CHOICES, default='1st')
    marks_obtained = models.FloatField()
    total_marks = models.FloatField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['student', 'subject', 'terminal']
        ordering = ['student__name', 'subject__name']

    def __str__(self):
        return f"{self.student.name} – {self.subject.name} ({self.get_terminal_display()}): {self.marks_obtained}"

    @property
    def percentage(self):
        if self.total_marks > 0:
            return round((self.marks_obtained / self.total_marks) * 100, 2)
        return 0

    @property
    def grade(self):
        gs = GradeScale.objects.filter(is_active=True).first()
        if gs:
            return gs.get_grade(self.percentage)
        return '-'

    @property
    def grade_point(self):
        gs = GradeScale.objects.filter(is_active=True).first()
        if gs:
            return gs.get_grade_point(self.percentage)
        return 0


# ─────────────────────────────────────────────────────────────────────────────
# 22. RESULT LOCK MODEL
# ─────────────────────────────────────────────────────────────────────────────
class ResultLock(models.Model):
    result = models.OneToOneField(Result, on_delete=models.CASCADE, related_name='lock')
    locked_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    locked_at = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=200, blank=True, default='')

    class Meta:
        ordering = ['-locked_at']

    def __str__(self):
        return f"Lock: {self.result.student.name} – {self.result.subject.name} ({self.result.terminal})"


# ─────────────────────────────────────────────────────────────────────────────
# 23. MESSAGE MODEL (Teacher ↔ Student messaging)
# ─────────────────────────────────────────────────────────────────────────────
class Message(models.Model):
    STATUS_CHOICES = [
        ('unread', 'Unread'),
        ('read', 'Read'),
    ]
    sender = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_messages')
    sender_student = models.ForeignKey('Student', on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_student_messages')
    recipient_student = models.ForeignKey('Student', on_delete=models.CASCADE, null=True, blank=True, related_name='received_messages')
    recipient_teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='received_teacher_messages')
    subject = models.CharField(max_length=200, default='', blank=True)
    user = models.TextField(blank=True, default='')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unread')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        sender_name = self.sender.get_full_name() if self.sender else (self.sender_student.name if self.sender_student else 'Unknown')
        recv_name = self.recipient_student.name if self.recipient_student else (self.recipient_teacher.get_full_name() if self.recipient_teacher else 'Unknown')
        return f"{sender_name} → {recv_name}: {self.subject}"


# ─────────────────────────────────────────────────────────────────────────────
# 24. STUDENT NOTE MODEL
# ─────────────────────────────────────────────────────────────────────────────
class StudentNote(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='student_notes')
    title = models.CharField(max_length=200, default='')
    content = models.TextField(default='', blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    created_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_notes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} — {self.student.name}"


# ─────────────────────────────────────────────────────────────────────────────
# 25. ML PREDICTION MODEL
# ─────────────────────────────────────────────────────────────────────────────
class MLPrediction(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='ml_predictions')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='ml_predictions')
    predicted_grade = models.CharField(max_length=10, blank=True)
    confidence_score = models.FloatField(default=0.0, help_text="Confidence 0–100")
    actual_grade = models.CharField(max_length=10, blank=True, help_text="Filled in when result is published")
    model_version = models.CharField(max_length=20, default='v1')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['student', 'subject', 'model_version']

    def __str__(self):
        return f"ML: {self.student.name} — {self.subject.name} → {self.predicted_grade}"


# ─────────────────────────────────────────────────────────────────────────────
# 26. SYSTEM CONFIG MODEL (Feature Flags)
# ─────────────────────────────────────────────────────────────────────────────
class SystemConfig(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.CharField(max_length=500, blank=True)
    description = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['key']

    def __str__(self):
        return self.key

    @classmethod
    def get_bool(cls, key, default=True):
        obj = cls.objects.filter(key=key).first()
        if obj:
            return obj.value.lower() in ('true', '1', 'yes', 'on')
        return default

    @classmethod
    def set_bool(cls, key, value, description=''):
        obj, _ = cls.objects.get_or_create(key=key, defaults={'description': description})
        obj.value = 'true' if value else 'false'
        obj.description = description or obj.description
        obj.save()
        return obj


# ─────────────────────────────────────────────────────────────────────────────
# 27. SUBSCRIPTION MODEL (A3 — Billing)
# ─────────────────────────────────────────────────────────────────────────────
PLAN_CHOICES = [
    ('starter', 'Starter'),
    ('pro', 'Pro'),
    ('enterprise', 'Enterprise'),
]

class Subscription(models.Model):
    institution = models.CharField(max_length=200, help_text="Institution / school name")
    plan = models.CharField(max_length=50, choices=PLAN_CHOICES, default='starter')
    monthly_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    auto_renew = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_subscriptions')

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.institution} — {self.get_plan_display()}"


# ─────────────────────────────────────────────────────────────────────────────
# 28. INVOICE MODEL (A3 — Billing)
# ─────────────────────────────────────────────────────────────────────────────
INVOICE_STATUS_CHOICES = [
    ('DRAFT', 'Draft'),
    ('SENT', 'Sent'),
    ('PAID', 'Paid'),
    ('OVERDUE', 'Overdue'),
    ('CANCELLED', 'Cancelled'),
]

from django.utils import timezone

def generate_invoice_number():
    last = Invoice.objects.order_by('-id').first()
    nxt = (last.id + 1) if last else 1
    return f"INV-{timezone.now().strftime('%Y%m%d')}-{nxt:04d}"

def invoice_number_default():
    return generate_invoice_number()

class Invoice(models.Model):
    invoice_number = models.CharField(max_length=50, unique=True, default=invoice_number_default)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    issued_to = models.CharField(max_length=200, blank=True)
    issue_date = models.DateField()
    due_date = models.DateField()
    paid_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=INVOICE_STATUS_CHOICES, default='DRAFT')
    line_items = models.JSONField(default=list, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    payment_link = models.URLField(blank=True)

    class Meta:
        ordering = ['-issue_date']

    def __str__(self):
        return f"{self.invoice_number} — {self.issued_to} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        self.total_amount = self.amount + self.tax_amount
        super().save(*args, **kwargs)


# ─────────────────────────────────────────────────────────────────────────────
# 29. CERTIFICATE TEMPLATE MODEL (A9)
# ─────────────────────────────────────────────────────────────────────────────
CERT_TYPE_CHOICES = [
    ('M', 'Mark Certificate'),
    ('TC', 'Transfer Certificate'),
    ('BON', 'Bonafide Certificate'),
    ('TR', 'Transfer'),
    ('ACH', 'Achievement'),
]

class CertificateTemplate(models.Model):
    name = models.CharField(max_length=100, unique=True)
    html_content = models.TextField(help_text="HTML with {{student.name}}, {{result_rows}} placeholders")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# ─────────────────────────────────────────────────────────────────────────────
# 30. CERTIFICATE MODEL (A9)
# ─────────────────────────────────────────────────────────────────────────────
CERT_STATUS_CHOICES = [
    ('DRAFT', 'Draft'),
    ('ISSUED', 'Issued'),
    ('REVOKED', 'Revoked'),
]

def generate_cert_number():
    last = Certificate.objects.order_by('-id').first()
    nxt = (last.id + 1) if last else 1
    return f"CERT-{timezone.now().strftime('%Y%m%d')}-{nxt:04d}"

class Certificate(models.Model):
    certificate_number = models.CharField(max_length=50, unique=True, default=generate_cert_number)
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='certificates')
    template = models.ForeignKey(CertificateTemplate, on_delete=models.PROTECT)
    certificate_type = models.CharField(max_length=30, choices=CERT_TYPE_CHOICES)
    issued_date = models.DateField(default=timezone.now)
    issued_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    qr_data_string = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=CERT_STATUS_CHOICES, default='DRAFT')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.certificate_number} — {self.student.name} ({self.get_certificate_type_display()})"


# ─────────────────────────────────────────────────────────────────────────────
# 31. API KEY MODEL (A14)
# ─────────────────────────────────────────────────────────────────────────────
def generate_api_key():
    raw = uuid.uuid4().hex + uuid.uuid4().hex
    return f"acad_{raw[:32]}"

class APIKey(models.Model):
    key = models.CharField(max_length=64, unique=True, default=generate_api_key)
    name = models.CharField(max_length=100)
    prefix = models.CharField(max_length=10, default='acad_')
    scopes = models.JSONField(default=list, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='api_keys')
    created_at = models.DateTimeField(auto_now_add=True)
    last_used_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    allowed_ips = models.JSONField(default=list, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.prefix}...)"


# ─────────────────────────────────────────────────────────────────────────────
# 32. WEBHOOK ENDPOINT MODEL (A14)
# ─────────────────────────────────────────────────────────────────────────────
def generate_webhook_secret():
    return uuid.uuid4().hex + uuid.uuid4().hex

class WebhookEndpoint(models.Model):
    url = models.URLField()
    secret = models.CharField(max_length=100, default=generate_webhook_secret)
    events = models.JSONField(default=list, blank=True)
    is_active = models.BooleanField(default=True)
    retry_count = models.PositiveIntegerField(default=3)
    last_triggered_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='webhook_endpoints')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.url


# ─────────────────────────────────────────────────────────────────────────────
# 33. WEBHOOK DELIVERY LOG MODEL (A14)
# ─────────────────────────────────────────────────────────────────────────────
class WebhookDeliveryLog(models.Model):
    endpoint = models.ForeignKey(WebhookEndpoint, on_delete=models.CASCADE, related_name='deliveries')
    event_type = models.CharField(max_length=50)
    payload = models.JSONField()
    response_code = models.PositiveIntegerField(null=True, blank=True)
    response_body = models.TextField(blank=True)
    success = models.BooleanField(default=False)
    attempt = models.PositiveIntegerField(default=1)
    delivered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-delivered_at']

    def __str__(self):
        return f"{self.endpoint.url} — {self.event_type} ({'✓' if self.success else '✗'})"


# ─────────────────────────────────────────────────────────────────────────────
# 34. SUPPORT TICKET MODEL (A5 — Bug Tracking)
# ─────────────────────────────────────────────────────────────────────────────
TICKET_CATEGORY_CHOICES = [
    ('Bug', 'Bug'),
    ('Feature', 'Feature Request'),
    ('Question', 'Question'),
    ('Other', 'Other'),
]
TICKET_PRIORITY_CHOICES = [
    ('Low', 'Low'),
    ('Medium', 'Medium'),
    ('High', 'High'),
    ('Critical', 'Critical'),
]
TICKET_STATUS_CHOICES = [
    ('Open', 'Open'),
    ('InProgress', 'In Progress'),
    ('Resolved', 'Resolved'),
    ('Closed', 'Closed'),
]

def generate_ticket_id():
    year = timezone.now().strftime('%Y')
    last = SupportTicket.objects.order_by('-id').first()
    nxt = (last.id + 1) if last else 1
    return f"TCK-{year}-{nxt:04d}"

class SupportTicket(models.Model):
    ticket_id = models.CharField(max_length=20, unique=True, default=generate_ticket_id)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=TICKET_CATEGORY_CHOICES, default='Other')
    priority = models.CharField(max_length=10, choices=TICKET_PRIORITY_CHOICES, default='Medium')
    status = models.CharField(max_length=20, choices=TICKET_STATUS_CHOICES, default='Open')
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_tickets')
    assigned_to = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_tickets')
    resolution_notes = models.TextField(blank=True)
    screenshot = models.ImageField(upload_to='tickets/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']


# ─────────────────────────────────────────────────────────────────────────────
# 35. TICKET COMMENT MODEL (A5)
# ─────────────────────────────────────────────────────────────────────────────
class TicketComment(models.Model):
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_internal = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']


# ─────────────────────────────────────────────────────────────────────────────
# 36. SSO PROVIDER MODEL (A10)
# ─────────────────────────────────────────────────────────────────────────────
SSO_TYPE_CHOICES = [
    ('oauth2', 'OAuth2'),
    ('saml', 'SAML'),
]

class SSOProvider(models.Model):
    name = models.CharField(max_length=50, unique=True)
    provider_type = models.CharField(max_length=20, choices=SSO_TYPE_CHOICES, default='oauth2')
    client_id = models.CharField(max_length=200, blank=True)
    client_secret = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# ─────────────────────────────────────────────────────────────────────────────
# 26. LICENSE KEY MODEL (A2 — Institutional Licensing)
# ─────────────────────────────────────────────────────────────────────────────
import uuid as _uuid


class LicenseKey(models.Model):
    key = models.CharField(max_length=64, unique=True, default=_uuid.uuid4)
    institution_name = models.CharField(max_length=200)
    max_teachers = models.PositiveIntegerField(default=5, help_text="Maximum teachers allowed")
    max_students = models.PositiveIntegerField(default=500, help_text="Maximum students allowed")
    max_branches = models.PositiveIntegerField(default=1, help_text="Maximum branches allowed")
    issued_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateField(null=True, blank=True, help_text="Leave blank for perpetual licence")
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='license_keys')
    current_teachers = models.PositiveIntegerField(default=0, help_text="Computed — do not edit manually")
    current_students = models.PositiveIntegerField(default=0, help_text="Computed — do not edit manually")
    current_branches = models.PositiveIntegerField(default=0, help_text="Computed — do not edit manually")
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-issued_at']

    def __str__(self):
        return f"{self.institution_name} — {self.key[:12]}…"

    def check_limits(self):
        """Return (ok, message) after checking all active counters against limits."""
        issues = []
        if self.current_teachers > self.max_teachers:
            issues.append(f"Teachers: {self.current_teachers}/{self.max_teachers} (over limit)")
        if self.current_students > self.max_students:
            issues.append(f"Students: {self.current_students}/{self.max_students} (over limit)")
        if self.current_branches > self.max_branches:
            issues.append(f"Branches: {self.current_branches}/{self.max_branches} (over limit)")
        if issues:
            return False, '; '.join(issues)
        return True, "Within limits"

    def refresh_counts(self):
        self.current_teachers = Teacher.objects.filter(is_active=True).count()
        self.current_students = Student.objects.filter().count()
        self.current_branches = 1   # Single-branch default; plug in Branch model when added
        self.save(update_fields=['current_teachers', 'current_students', 'current_branches'])


class SystemConfig(models.Model):
    """Key-value configuration store persisted in the database."""
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['key']

    def __str__(self):
        return self.key

    @classmethod
    def get(cls, key, default=''):
        obj = cls.objects.filter(key=key).first()
        return obj.value if obj else default

    @classmethod
    def set(cls, key, value):
        obj, _ = cls.objects.update_or_create(key=key, defaults={'value': str(value)})
        return obj


# ─────────────────────────────────────────────────────────────────────────────
# 27. RBAC 2.0 — ROLE & PERMISSION MODELS (A6)
# ─────────────────────────────────────────────────────────────────────────────

ROLE_CHOICES = [
    ('super_admin', 'Super Admin'),
    ('admin', 'Administrator'),
    ('teacher', 'Teacher'),
    ('finance', 'Finance Officer'),
    ('librarian', 'Librarian'),
    ('registrar', 'Registrar'),
    ('viewer', 'Viewer'),
]


class UserRole(models.Model):
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=20, unique=True, choices=ROLE_CHOICES)
    description = models.TextField(blank=True)
    can_manage_students = models.BooleanField(default=False)
    can_manage_teachers = models.BooleanField(default=False)
    can_manage_subjects = models.BooleanField(default=False)
    can_manage_fees = models.BooleanField(default=False)
    can_manage_exams = models.BooleanField(default=False)
    can_manage_attendance = models.BooleanField(default=False)
    can_manage_materials = models.BooleanField(default=False)
    can_view_reports = models.BooleanField(default=False)
    can_manage_system = models.BooleanField(default=False)
    is_system_role = models.BooleanField(default=False, help_text="Cannot be deleted")

    class Meta:
        ordering = ['code']

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='profile')
    role = models.ForeignKey(UserRole, on_delete=models.PROTECT)
    branch = models.ForeignKey('Branch', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['user__username']

    def __str__(self):
        return f"{self.user.username} — {self.role.name}"


# ─────────────────────────────────────────────────────────────────────────────
# 28. BACKUP & RESTORE MODEL (A7)
# ─────────────────────────────────────────────────────────────────────────────

BACKUP_TYPE_CHOICES = [
    ('database', 'Database (pg_dump)'),
    ('django_export', 'Django Serialized (JSON)'),
]

BACKUP_STATUS_CHOICES = [
    ('in_progress', 'In Progress'),
    ('success', 'Success'),
    ('failed', 'Failed'),
]


class SystemBackup(models.Model):
    filename = models.CharField(max_length=255)
    size_bytes = models.PositiveBigIntegerField(default=0)
    backup_type = models.CharField(max_length=20, choices=BACKUP_TYPE_CHOICES, default='django_export')
    triggered_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='system_backups')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=BACKUP_STATUS_CHOICES, default='in_progress')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.filename} ({self.status}) — {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    @property
    def size_display(self):
        if self.size_bytes < 1024:
            return f"{self.size_bytes} B"
        elif self.size_bytes < 1024 ** 2:
            return f"{round(self.size_bytes / 1024, 1)} KB"
        elif self.size_bytes < 1024 ** 3:
            return f"{round(self.size_bytes / 1024 ** 2, 1)} MB"
        return f"{round(self.size_bytes / 1024 ** 3, 1)} GB"


# ─────────────────────────────────────────────────────────────────────────────
# 29. PARENT USER — PORTAL ACCOUNT (A11)
# ─────────────────────────────────────────────────────────────────────────────

class ParentUser(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='parent_profile')
    parent = models.OneToOneField(Parent, on_delete=models.CASCADE, related_name='user_account')
    phone = models.CharField(max_length=15, blank=True)
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=255, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['user__username']

    def __str__(self):
        return f"Portal: {self.user.username} → Parent of {self.parent.student.name}"


# ─────────────────────────────────────────────────────────────────────────────
# 30. RESULT PUBLICATION WORKFLOW MODELS (A13)
# ─────────────────────────────────────────────────────────────────────────────

PUBLISH_STATUS_CHOICES = [
    ('draft', 'Draft'),
    ('under_review', 'Under Review'),
    ('approved', 'Approved'),
    ('published', 'Published'),
    ('rejected', 'Rejected'),
    ('archived', 'Archived'),
]


class ResultPublishSession(models.Model):
    name = models.CharField(max_length=200, help_text="e.g. 1st Terminal 2025")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='publish_sessions')
    target_class = models.CharField(max_length=20, help_text="Class for which results are published")
    academic_year = models.ForeignKey(AcademicYear, null=True, blank=True, on_delete=models.SET_NULL, related_name='publish_sessions')
    status = models.CharField(max_length=20, choices=PUBLISH_STATUS_CHOICES, default='draft')
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='created_publish_sessions')
    reviewed_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_sessions')
    approved_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_sessions')
    published_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Result Publish Session'
        verbose_name_plural = 'Result Publish Sessions'

    def __str__(self):
        return f"{self.name} — {self.subject.name} ({self.target_class}) [{self.status}]"


class ResultSessionEntry(models.Model):
    session = models.ForeignKey(ResultPublishSession, on_delete=models.CASCADE, related_name='entries')
    result = models.ForeignKey(Result, on_delete=models.CASCADE)
    is_locked = models.BooleanField(default=False, help_text="Individual entry-level lock within session")

    class Meta:
        unique_together = ['session', 'result']
        ordering = ['session', 'result__student__name']

    def __str__(self):
        return f"Session: {self.session.name} — {self.result.student.name} / {self.result.subject.name}"



# ═════════════════════════════════════════════════════════════════════════════
# T2 — LESSON PLAN & SYLLABUS TRACKER
# ═════════════════════════════════════════════════════════════════════════════

TEACHING_METHOD_CHOICES = [
    ('lecture', 'Lecture'),
    ('discussion', 'Discussion'),
    ('practical', 'Practical'),
    ('group', 'Group Work'),
    ('flipclass', 'Flip Class'),
]

LESSON_STATUS_CHOICES = [
    ('planned', 'Planned'),
    ('completed', 'Completed'),
    ('skipped', 'Skipped'),
]

SYLLABUS_ARRANGEMENT_CHOICES = [
    ('row_wise', 'Row Wise'),
    ('column_wise', 'Column Wise'),
    ('checkerboard', 'Checkerboard'),
]


class LessonPlan(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='lesson_plans')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    class_section = models.CharField(max_length=20, help_text="e.g. '10A', 'XI-B'")
    chapter_topic = models.CharField(max_length=200)
    planned_date = models.DateField()
    actual_date = models.DateField(null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(default=45)
    teaching_method = models.CharField(max_length=50, choices=TEACHING_METHOD_CHOICES, default='lecture')
    learning_outcomes = models.TextField(blank=True)
    resources_used = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=LESSON_STATUS_CHOICES, default='planned')
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-planned_date', '-created_at']
        indexes = [
            models.Index(fields=['teacher', 'subject', 'planned_date']),
        ]

    def __str__(self):
        return f"{self.title} — {self.subject.name} ({self.class_section}) [{self.get_status_display()}]"


class SyllabusCoverage(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='syllabus_items')
    class_section = models.CharField(max_length=20)
    chapter_name = models.CharField(max_length=200)
    estimated_hours = models.PositiveIntegerField(default=2)
    actual_hours = models.PositiveIntegerField(default=0)
    planned_order = models.PositiveIntegerField(default=1)
    is_completed = models.BooleanField(default=False)
    completion_pct = models.PositiveIntegerField(default=0, help_text="0-100, computed from related LessonPlans")
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['subject__name', 'class_section', 'planned_order']
        unique_together = ['subject', 'class_section', 'chapter_name']
        indexes = [
            models.Index(fields=['subject', 'class_section']),
        ]

    def __str__(self):
        return f"{self.subject.name} — {self.class_section} — {self.chapter_name}"

    def update_completion_pct(self):
        related = LessonPlan.objects.filter(subject=self.subject, class_section=self.class_section)
        total = related.count()
        completed = related.filter(status='completed').count()
        pct = round((completed / total * 100)) if total > 0 else 0
        self.completion_pct = pct
        self.is_completed = completed == total and total > 0
        self.save(update_fields=['completion_pct', 'is_completed'])


# ═════════════════════════════════════════════════════════════════════════════
# T3 — TWO-WAY GRADING RUBRICS
# ═════════════════════════════════════════════════════════════════════════════

class GradingRubric(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='rubrics')
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} — {self.teacher.get_full_name()}"


class RubricCriterion(models.Model):
    rubric = models.ForeignKey(GradingRubric, on_delete=models.CASCADE, related_name='criteria')
    name = models.CharField(max_length=100, help_text="e.g. 'Accuracy', 'Presentation', 'Neatness'")
    max_score = models.FloatField(default=10.0)
    weight_percent = models.FloatField(default=33.3, help_text="% of total grade")
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']
        unique_together = ['rubric', 'name']

    def __str__(self):
        return f"{self.rubric.name} — {self.name} (max {self.max_score})"


class RubricScoreEntry(models.Model):
    submission = models.ForeignKey(AssignmentSubmission, on_delete=models.CASCADE, related_name='rubric_scores')
    criterion = models.ForeignKey(RubricCriterion, on_delete=models.CASCADE)
    score_obtained = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['criterion__order']
        unique_together = ['submission', 'criterion']

    def __str__(self):
        return f"{self.submission} — {self.criterion.name}: {self.score_obtained}/{self.criterion.max_score}"


class RubricTemplate(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_global = models.BooleanField(default=False, help_text="Available to all teachers")
    criteria_data = models.JSONField(help_text="List of {name, max_score, weight_percent}")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{'🌍 ' if self.is_global else '📋 '}{self.name}"


# ═════════════════════════════════════════════════════════════════════════════
# T4 — ONLINE EXAM / QUIZ MODULE
# ═════════════════════════════════════════════════════════════════════════════

QUESTION_TYPE_CHOICES = [
    ('MCQ', 'Multiple Choice'),
    ('TRUE_FALSE', 'True / False'),
    ('SHORT_ANSWER', 'Short Answer'),
    ('LONG_ANSWER', 'Long Answer'),
]

ATTEMPT_STATUS_CHOICES = [
    ('IN_PROGRESS', 'In Progress'),
    ('SUBMITTED', 'Submitted'),
    ('TIMED_OUT', 'Timed Out'),
]


class OnlineExam(models.Model):
    title = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='online_exams')
    target_class = models.CharField(max_length=20)
    target_section = models.CharField(max_length=5, blank=True)
    total_marks = models.PositiveIntegerField(default=100)
    passing_marks = models.PositiveIntegerField(default=40)
    duration_minutes = models.PositiveIntegerField(default=60)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    is_published = models.BooleanField(default=False)
    show_result_immediately = models.BooleanField(default=True)
    shuffle_questions = models.BooleanField(default=True)
    max_attempts = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_at']
        indexes = [
            models.Index(fields=['subject', 'is_published', 'start_at']),
        ]

    def __str__(self):
        return f"{self.title} — {self.subject.name} ({self.target_class})"

    @property
    def is_available(self):
        now = timezone.now()
        return self.is_published and self.start_at <= now <= self.end_at

    @property
    def has_ended(self):
        return timezone.now() > self.end_at


class Question(models.Model):
    online_exam = models.ForeignKey(OnlineExam, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES, default='MCQ')
    options = models.JSONField(default=list, blank=True, help_text="For MCQ: list of {label, text}")
    correct_answer = models.CharField(max_length=500, blank=True, help_text="MCQ: 'A' | TF: 'True'/'False'")
    marks = models.PositiveIntegerField(default=1)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']
        indexes = [
            models.Index(fields=['online_exam', 'order']),
        ]

    def __str__(self):
        return f"Q{self.order}: {self.question_text[:60]}..."


class ExamAttempt(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='exam_attempts')
    online_exam = models.ForeignKey(OnlineExam, on_delete=models.CASCADE, related_name='attempts')
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    score_obtained = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=ATTEMPT_STATUS_CHOICES, default='IN_PROGRESS')
    attempt_number = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['-started_at']
        unique_together = ['student', 'online_exam', 'attempt_number']

    def __str__(self):
        return f"{self.student.name} — {self.online_exam.title} (Attempt {self.attempt_number})"


class ExamAnswer(models.Model):
    attempt = models.ForeignKey(ExamAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField(blank=True)
    selected_option = models.CharField(max_length=10, blank=True, help_text="'A'/'B'/'C'/'D'")
    marks_awarded = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['question__order']
        unique_together = ['attempt', 'question']

    def __str__(self):
        return f"{self.attempt} — Q{self.question.order}: {self.selected_option or self.answer_text[:30]}"


# ═════════════════════════════════════════════════════════════════════════════
# T5 — SEATING PLAN & HALL TICKET GENERATOR
# ═════════════════════════════════════════════════════════════════════════════

class ExamSeatingPlan(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='seating_plan')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    room_name = models.CharField(max_length=100, help_text="Room A, Hall 1, etc.")
    room_capacity = models.PositiveIntegerField(default=30)
    arrangement_type = models.CharField(max_length=20, choices=SYLLABUS_ARRANGEMENT_CHOICES, default='row_wise')
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.room_name} — {self.exam.title}"


class SeatAllocation(models.Model):
    seating_plan = models.ForeignKey(ExamSeatingPlan, on_delete=models.CASCADE, related_name='allocations')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10, help_text="e.g. 'A-01', 'B-15'")
    row = models.PositiveIntegerField()
    column = models.PositiveIntegerField()
    is_present = models.BooleanField(null=True, blank=True)
    is_locked = models.BooleanField(default=False, help_text="Locked after attendance taken")
    notes = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['row', 'column']
        unique_together = ['seating_plan', 'seat_number']

    def __str__(self):
        return f"{self.seat_number} — {self.student.name} ({self.seating_plan})"


# ═════════════════════════════════════════════════════════════════════════════
# T6 — TEACHER LEAVE MANAGEMENT
# ═════════════════════════════════════════════════════════════════════════════

LEAVE_TYPE_CHOICES = [
    ('casual', 'Casual Leave'),
    ('sick', 'Sick Leave'),
    ('annual', 'Annual Leave'),
    ('emergency', 'Emergency Leave'),
]

LEAVE_STATUS_CHOICES = [
    ('PENDING', 'Pending'),
    ('APPROVED', 'Approved'),
    ('REJECTED', 'Rejected'),
    ('CANCELLED', 'Cancelled'),
]


class TeacherLeave(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE_CHOICES, default='casual')
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    substitute_teacher = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='substitute_assignments'
    )
    status = models.CharField(max_length=20, choices=LEAVE_STATUS_CHOICES, default='PENDING')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_leaves')
    approval_reason = models.TextField(blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['teacher', 'status', 'start_date']),
        ]

    def __str__(self):
        return f"{self.teacher.get_full_name()} — {self.get_leave_type_display()} ({self.start_date} → {self.end_date}) [{self.status}]"

    @property
    def days_count(self):
        from datetime import timedelta
        if not self.start_date or not self.end_date:
            return 0
        delta = self.end_date - self.start_date
        return delta.days + 1

    def save(self, *args, **kwargs):
        self.days_count = self.days_count  # computed property
        super().save(*args, **kwargs)


# ═════════════════════════════════════════════════════════════════════════════════╗
# T8  SMART QUESTION BANK                                                          ║
# T9  REMINDER SCHEDULER                                                           ║
# ═════════════════════════════════════════════════════════════════════════════════╝

# ── shared choice lists ──────────────────────────────────────────────────────────

QUESTION_TYPE_CHOICES = [
    ('mcq', 'Multiple Choice'),
    ('true_false', 'True / False'),
    ('short_answer', 'Short Answer'),
    ('long_answer', 'Long Answer'),
]

DIFFICULTY_CHOICES = [
    ('easy', 'Easy'),
    ('medium', 'Medium'),
    ('hard', 'Hard'),
]

REMINDER_TYPE_CHOICES = [
    ('assignment_deadline', 'Assignment Deadline'),
    ('attendance', 'Attendance'),
    ('meeting', 'Meeting'),
    ('fee', 'Fee'),
    ('study', 'Study'),
    ('custom', 'Custom'),
]

RECURRENCE_CHOICES = [
    ('none', 'One-time'),
    ('daily', 'Daily'),
    ('weekly', 'Weekly'),
    ('monthly', 'Monthly'),
]

SCHEDULED_TASK_TYPE_CHOICES = [
    ('reminder', 'Reminder'),
    ('sms_digest', 'SMS / Email Digest'),
    ('fee_alert', 'Fee Alert'),
    ('certificate_expiry', 'Certificate Expiry'),
]

# ─────────────────────────────────────────────────────────────────────────────────
# T8. QUESTION BANK
# ─────────────────────────────────────────────────────────────────────────────────
class QuestionBank(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='question_bank')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='question_bank')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES)
    options = models.JSONField(default=list, blank=True,
                               help_text='List of {"key":"A","text":"…"} dicts for MCQ/True-False')
    correct_answer = models.CharField(max_length=500)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='medium')
    chapter = models.CharField(max_length=100)
    marks = models.PositiveIntegerField(default=1)
    tags = models.CharField(max_length=200, blank=True, help_text='Comma-separated tags')
    is_active = models.BooleanField(default=True)
    times_used = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['subject', 'difficulty']),
            models.Index(fields=['chapter']),
        ]

    def __str__(self):
        return f"{self.subject.code} | {self.get_difficulty_display()} | {self.question_text[:60]}"


# ─────────────────────────────────────────────────────────────────────────────────
# T8. QUESTION PAPER TEMPLATE
# ─────────────────────────────────────────────────────────────────────────────────
class QuestionPaperTemplate(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    total_marks = models.PositiveIntegerField()
    duration_minutes = models.PositiveIntegerField()
    distribution = models.JSONField(
        help_text='{"easy": N, "medium": N, "hard": N} number of questions per difficulty'
    )
    chapters = models.JSONField(default=list, blank=True,
                                help_text='List of chapter strings to include')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE,
                                related_name='paper_templates')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} – {self.subject.name} ({self.total_marks} marks)"


# ─────────────────────────────────────────────────────────────────────────────────
# T9.  REMINDER
# ─────────────────────────────────────────────────────────────────────────────────
class Reminder(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='reminders')
    student = models.ForeignKey('Student', on_delete=models.CASCADE, null=True, blank=True,
                                related_name='reminders')
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    reminder_type = models.CharField(max_length=30, choices=REMINDER_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    scheduled_for = models.DateTimeField()
    recurrence = models.CharField(max_length=20, choices=RECURRENCE_CHOICES, default='none')
    recurrence_until = models.DateField(null=True, blank=True)
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['scheduled_for']

    def __str__(self):
        return f"{self.title} → {self.get_reminder_type_display()} @ {self.scheduled_for.strftime('%Y-%m-%d %H:%M')}"


# ─────────────────────────────────────────────────────────────────────────────────
# T9.  SCHEDULED TASK  (replaces Celery/cron with polling)
# ─────────────────────────────────────────────────────────────────────────────────
class ScheduledTask(models.Model):
    task_type = models.CharField(max_length=30, choices=SCHEDULED_TASK_TYPE_CHOICES)
    scheduled_for = models.DateTimeField()
    payload = models.JSONField(default=dict, blank=True)
    is_executed = models.BooleanField(default=False)
    executed_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['scheduled_for']

    def __str__(self):
        return f"{self.get_task_type_display()} @ {self.scheduled_for.strftime('%Y-%m-%d %H:%M')}"


# ═══════════════════════════════════════════════════════════════════════════════════
# ══ SECTION B — ALL MISSING FEATURE MODELS  ════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════════════════════════

# ╔══════════════════════════════════════════════════════════════════════════════════╗
# ║  ──── 1. SMART ATTENDANCE SYSTEM ──────────────────────────────────────────────║
# ╚══════════════════════════════════════════════════════════════════════════════════╝
# 1-A · QR Code Attendance
# ─────────────────────────

class QRCodeAttendance(models.Model):
    """Attendance entries verified via teacher-scanned QR code."""
    ATTENDANCE_STATUS = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    ]
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='qr_attendance')
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=ATTENDANCE_STATUS, default='present')
    qr_data = models.CharField(max_length=255, blank=True, help_text="URL encoded in QR at scan time")
    token = models.CharField(max_length=64, unique=True, help_text="Time-limited token for QR verification")
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    recorded_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']
        indexes = [models.Index(fields=['student', 'date']), models.Index(fields=['token'])]

    def __str__(self):
        return f"QR: {self.student.name} — {self.date} — {self.get_status_display()}"


# 1-B · Face Recognition Attendance
# ────────────────────────────────────

class FaceAttendance(models.Model):
    """Attendance entries confirmed via facial recognition (webcam/photo)."""
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='face_attendance')
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    recognized = models.BooleanField(default=True, help_text="Was the student's face successfully recognized?")
    match_score = models.FloatField(default=0.0, help_text="Facial recognition confidence 0–100")
    reference_image_url = models.URLField(blank=True, null=True)
    captured_image_url = models.URLField(blank=True, null=True)
    is_present = models.BooleanField(default=False, help_text="Verified present if recognized=True")
    status = models.CharField(max_length=15, default='present', choices=[
        ('present', 'Present'), ('absent', 'Absent'), ('doubt', 'Needs Manual Review'),
    ])
    geofence_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    geofence_lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    recorded_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']
        indexes = [models.Index(fields=['student', 'date'])]

    def __str__(self):
        s, conf = self.status, self.match_score
        return f"Face: {self.student.name} — {self.date} [{s}] ({conf}%)"


# 1-C · GPS-based Attendance Verification
# ──────────────────────────────────────────

class GPSAttendance(models.Model):
    """Location-verified attendance entries."""
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='gps_attendance')
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    check_in_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    check_in_lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    check_out_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    check_out_lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    geofence_radius_m = models.PositiveIntegerField(default=100, help_text="Allowed radius in metres")
    # Decode HS (Haversine) distance so we know if student was inside
    distance_m = models.FloatField(null=True, blank=True, help_text="Distance in metres from school centroid")
    is_within_geofence = models.BooleanField(default=False)
    status = models.CharField(max_length=10, default='present', choices=[
        ('present', 'Present'), ('absent', 'Absent'), ('incomplete', 'Check-in Only'),
    ])
    device_info = models.CharField(max_length=255, blank=True)
    recorded_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', 'student__name']
        indexes = [models.Index(fields=['student', 'date'])]

    def __str__(self):
        return f"GPS: {self.student.name} — {self.date} — {self.get_status_display()}"


# 1-D · Late Entry Tracking
# ──────────────────────────

class LateEntryLog(models.Model):
    LATE_REASON_CHOICES = [
        ('traffic', 'Traffic'), ('accident', 'Accident'),
        ('sick', 'Sick / Medical'), ('family', 'Family Emergency'),
        ('vehicle', 'Vehicle Issue'), ('public_transport', 'Public Transport Delay'),
        ('other', 'Other'),
    ]
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='late_entries')
    date = models.DateField()
    expected_arrival = models.TimeField(null=True, blank=True)
    actual_arrival = models.TimeField(null=True, blank=True)
    minutes_late = models.PositiveIntegerField(default=0)
    reason = models.CharField(max_length=30, choices=LATE_REASON_CHOICES, default='other')
    reason_detail = models.TextField(blank=True)
    is_excused = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False, help_text="Parent / admin verified")
    is_active = models.BooleanField(default=True, help_text="Show on attendance report")
    notified_parent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', 'student__name']
        indexes = [models.Index(fields=['student', 'date'])]

    def __str__(self):
        return f"Late: {self.student.name} — {self.date} ({self.minutes_late} min)"


# 1-E · Auto-generated Attendance Report
# ─────────────────────────────────────────

class AttendanceReport(models.Model):
    REPORT_TYPE_CHOICES = [
        ('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly'),
        ('termwise', 'Term-wise'), ('custom', 'Custom Range'),
    ]
    STATUS_CHOICES = [('draft', 'Draft'), ('final', 'Final'), ('archived', 'Archived')]
    title = models.CharField(max_length=200)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    target_class = models.CharField(max_length=20, blank=True)
    target_section = models.CharField(max_length=5, default='')
    student = models.ForeignKey('Student', on_delete=models.SET_NULL, null=True, blank=True,
                                help_text="Leave blank for class-level report")
    start_date = models.DateField()
    end_date = models.DateField()
    total_present = models.PositiveIntegerField(default=0)
    total_absent = models.PositiveIntegerField(default=0)
    total_late = models.PositiveIntegerField(default=0)
    total_excused = models.PositiveIntegerField(default=0)
    attendance_percentage = models.FloatField(default=0.0)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='draft')
    notes = models.TextField(blank=True)
    generated_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date', '-created_at']

    def __str__(self):
        return f"Attn Report: {self.title} — {self.start_date} to {self.end_date}"


# ╔══════════════════════════════════════════════════════════════════════════════════╗
# ║  ──── 3. ASSIGNMENT ENHANCEMENTS ──────────────────────────────────────────────║
# ╚══════════════════════════════════════════════════════════════════════════════════╝
# 3-A · Plagiarism Detection
# ───────────────────────────

class PlagiarismReport(models.Model):
    PLAGIARISM_RISK_CHOICES = [
        ('low', 'Low Risk (< 20%)'), ('medium', 'Moderate (20-50%)'),
        ('high', 'High Risk (50-80%)'), ('critical', 'Critical (> 80%)'),
    ]
    submission = models.ForeignKey(AssignmentSubmission, on_delete=models.CASCADE,
                                   related_name='plagiarism_check')
    overall_similarity = models.FloatField(default=0.0, help_text="Overall text similarity %")
    risk_level = models.CharField(max_length=20, choices=PLAGIARISM_RISK_CHOICES, default='low')
    matching_sources = models.JSONField(default=list, blank=True,
                                        help_text="List of matching URLs / document names")
    highlighted_text = models.TextField(blank=True, help_text="Text excerpts that were flagged")
    word_count = models.PositiveIntegerField(default=0)
    is_final = models.BooleanField(default=True)
    checked_at = models.DateTimeField(auto_now_add=True)
    checked_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True,
                                   help_text="Manual flag by teacher")

    class Meta:
        ordering = ['-checked_at']

    def __str__(self):
        return f"Plagiarism: Sub #{self.submission.id} — {self.overall_similarity}% ({self.risk_level})"


# 3-B · MCQ Auto-Grading
# ─────────────────────────

class MCQAutoGrade(models.Model):
    submission = models.ForeignKey(AssignmentSubmission, on_delete=models.CASCADE,
                                   related_name='mcq_grades')
    total_mcqs = models.PositiveIntegerField(default=0)
    correct = models.PositiveIntegerField(default=0)
    incorrect = models.PositiveIntegerField(default=0)
    not_answered = models.PositiveIntegerField(default=0)
    marks_earned = models.FloatField(default=0.0)
    marks_possible = models.FloatField(default=0.0)
    score_percentage = models.FloatField(default=0.0)
    answers_detail = models.JSONField(default=dict, blank=True,
                                      help_text="Per-question answer breakdown")
    auto_graded_at = models.DateTimeField(auto_now_add=True)
    auto_graded = models.BooleanField(default=True)

    class Meta:
        ordering = ['-auto_graded_at']

    def __str__(self):
        return f"Auto-grade: Sub #{self.submission.id} — {self.score_percentage}%"

    def save(self, *args, **kwargs):
        self.score_percentage = round((self.marks_earned / self.marks_possible * 100), 1) \
            if self.marks_possible > 0 else 0.0
        super().save(*args, **kwargs)


# ╔══════════════════════════════════════════════════════════════════════════════════╗
# ║  ──── 4. LIVE CLASSROOM SYSTEM ───────────────────────────────────────────────║
# ╚══════════════════════════════════════════════════════════════════════════════════╝

class LiveClass(models.Model):
    LIVE_STATUS_CHOICES = [
        ('scheduled', 'Scheduled'), ('ongoing', 'Ongoing'), ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='live_classes')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='live_classes')
    target_class = models.CharField(max_length=20)
    target_section = models.CharField(max_length=5, default='')
    scheduled_at = models.DateTimeField()
    ended_at = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(default=60)
    meeting_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    meeting_link = models.URLField(blank=True, null=True)
    meeting_password = models.CharField(max_length=50, blank=True)
    allow_screen_share = models.BooleanField(default=True)
    allow_whiteboard = models.BooleanField(default=True)
    allow_chat = models.BooleanField(default=False, help_text="Student-to-teacher chat during class")
    is_published = models.BooleanField(default=False)
    recording_url = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=15, choices=LIVE_STATUS_CHOICES, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-scheduled_at']

    def __str__(self):
        return f"{self.title} — {self.subject.name} ({self.get_status_display()})"

    @property
    def is_running(self):
        now = timezone.now()
        return self.status == 'ongoing' and self.scheduled_at <= now


class LiveClassAttendance(models.Model):
    live_class = models.ForeignKey(LiveClass, on_delete=models.CASCADE, related_name='attendances')
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='live_attendances')
    joined_at = models.DateTimeField(null=True, blank=True)
    left_at = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(default=0, help_text="Auto‑computed or manual override")
    is_present = models.BooleanField(default=False, help_text="True if joined & stayed > 1 min")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-joined_at']
        unique_together = ['live_class', 'student']

    def __str__(self):
        return f"LiveClass Att: {self.student.name} — {self.live_class.title}"


class LiveClassRecording(models.Model):
    live_class = models.ForeignKey(LiveClass, on_delete=models.CASCADE, related_name='recordings')
    video_file = models.FileField(upload_to='live_class_recordings/', null=True, blank=True)
    external_url = models.URLField(blank=True, null=True)
    file_size_mb = models.FloatField(default=0.0)
    duration_seconds = models.PositiveIntegerField(default=0)
    recorded_at = models.DateTimeField(auto_now_add=True)
    is_transcribed = models.BooleanField(default=False)
    transcript_file = models.FileField(upload_to='live_class_transcripts/', null=True, blank=True)

    class Meta:
        ordering = ['-recorded_at']

    def __str__(self):
        return f"Recording: {self.live_class.title} — {self.recorded_at.strftime('%Y-%m-%d')}"


# ╔══════════════════════════════════════════════════════════════════════════════════╗
# ║  ──── 5. EXAM ENHANCEMENT — RECHECKING ───────────────────────────────────────║
# ╚══════════════════════════════════════════════════════════════════════════════════╝

class RecheckingRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'), ('in_progress', 'In Progress'),
        ('accepted', 'Accepted — Marks Updated'), ('rejected', 'Rejected'),
        ('closed', 'Closed'),
    ]
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='rechecking_requests')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='rechecking_requests')
    terminal = models.CharField(max_length=10, default='1st')
    old_marks = models.FloatField(help_text="Existing marks before review")
    reason = models.TextField(help_text="Why should marks be rechecked?")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    new_marks = models.FloatField(null=True, blank=True, help_text="Updated by teacher/admin")
    review_notes = models.TextField(blank=True, help_text="Teacher / admin review explanation")
    reviewed_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='reviewed_recheckings')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['student', 'subject', 'terminal']

    def __str__(self):
        return f"Recheck: {self.student.name} — {self.subject.name} ({self.terminal}) [{self.status}]"


# ╔══════════════════════════════════════════════════════════════════════════════════╗
# ║  ──── 6. STUDENT BEHAVIOR MONITORING ─────────────────────────────────────────║
# ╚══════════════════════════════════════════════════════════════════════════════════╝

class DisciplineRecord(models.Model):
    SEVERITY_CHOICES = [
        ('minor', 'Minor'), ('moderate', 'Moderate'), ('serious', 'Serious'), ('major', 'Major'),
    ]
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='discipline_records')
    date = models.DateField()
    description = models.CharField(max_length=255)
    detail = models.TextField(blank=True)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='minor')
    action_taken = models.TextField(blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    points_deducted = models.IntegerField(default=0, help_text="Behavior score impact")
    parent_notified = models.BooleanField(default=False, help_text="Parent was sent notification")
    parent_notified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"Discipline: {self.student.name} — {self.date} [{self.severity}]"


class ParticipationScore(models.Model):
    SESSION_TYPE_CHOICES = [
        ('live_class', 'Live Class'), ('assignment', 'Assignment Submitted'),
        ('quiz', 'Quiz Attempted'), ('forum', 'Forum Post'), ('class_participation', 'Class Participation'),
    ]
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='participation_scores')
    session_type = models.CharField(max_length=30, choices=SESSION_TYPE_CHOICES)
    reference_id = models.PositiveIntegerField(null=True, blank=True, help_text="ID of related object")
    session_date = models.DateField()
    score_earned = models.PositiveIntegerField(default=0, help_text="XP earned")
    score_possible = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-session_date', '-created_at']

    def __str__(self):
        return f"Participation: {self.student.name} — {self.get_session_type_display()} (+{self.score_earned})"


# 6-C · Behavioral Analytics (computed abuse patterns)
# ────────────────────────────────────────────────────

class BehavioralAnalytics(models.Model):
    student = models.OneToOneField('Student', on_delete=models.CASCADE, related_name='behavior_analytics')
    total_discipline_points = models.IntegerField(default=0, help_text="Negative points")
    total_participation_points = models.IntegerField(default=0, help_text="Positive participation XP")
    behavior_score = models.FloatField(default=0.0, help_text="= base 100 + participation − discipline")
    attendance_risk = models.CharField(max_length=20, default='low', choices=[
        ('low', 'Low'), ('medium', 'Medium'), ('high', 'High'),
    ])
    attendance_risk_score = models.FloatField(default=0.0, help_text="0 = no risk, 100 = very high risk")
    academic_risk = models.CharField(max_length=20, default='low', choices=[
        ('low', 'Low'), ('medium', 'Medium'), ('high', 'High'),
    ])
    behavioral_risk = models.CharField(max_length=20, default='low', choices=[
        ('low', 'Low'), ('medium', 'Medium'), ('high', 'High'),
    ])
    last_calculated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-behavior_score']

    def __str__(self):
        return f"Analytics: {self.student.name} — Score {self.behavior_score}"


# ╔══════════════════════════════════════════════════════════════════════════════════╗
# ║  ──── 9. SMART TIMETABLE GENERATOR ──────────────────────────────────────────║
# ╚══════════════════════════════════════════════════════════════════════════════════╝

class Timetable(models.Model):
    STATUS_CHOICES = [('draft', 'Draft'), ('active', 'Active'), ('archived', 'Archived')]
    title = models.CharField(max_length=200, help_text="e.g. 2025, Semester 1")
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='timetables')
    level = models.CharField(max_length=20, choices=EducationLevel.LEVEL_CHOICES)
    student_class = models.CharField(max_length=20, help_text="e.g. 10, XI, S1")
    section = models.CharField(max_length=5, default='')
    semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True, blank=True)
    generated_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='draft')
    auto_generated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-academic_year__start_date', 'student_class']

    def __str__(self):
        return f"TT: {self.title} — {self.level} {self.student_class} {self.section}"


class TimetableEntry(models.Model):
    DAY_CHOICES = [
        ('sun', 'Sunday'), ('mon', 'Monday'), ('tue', 'Tuesday'),
        ('wed', 'Wednesday'), ('thu', 'Thursday'), ('fri', 'Friday'), ('sat', 'Saturday'),
    ]
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, related_name='entries')
    day = models.CharField(max_length=15, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    room = models.CharField(max_length=50, blank=True)
    notes = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['day', 'start_time']
        unique_together = ['timetable', 'day', 'start_time', 'subject']

    def __str__(self):
        return f"{self.get_day_display()} {self.start_time.strftime('%H:%M')}–{self.end_time.strftime('%H:%M')}: {self.subject or '—'}"


class TimetableConflict(models.Model):
    CONFLICT_LEVEL_CHOICES = [
        ('info', 'Info'), ('warning', 'Warning'), ('critical', 'Critical'),
    ]
    timetable = models.ForeignKey(Timetable, on_delete=models.SET_NULL, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    day = models.CharField(max_length=15)
    start_time = models.TimeField()
    end_time = models.TimeField()
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    conflict_level = models.CharField(max_length=15, choices=CONFLICT_LEVEL_CHOICES, default='warning')
    message = models.TextField(blank=True)
    resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Conflict: {self.teacher.get_full_name() if self.teacher else 'Unknown'} — {self.get_day_display()} {self.start_time} ({self.conflict_level})"


# ── Exam Room (physical venue management) ────────────────────────────────────────

class ExamRoom(models.Model):
    name = models.CharField(max_length=100, unique=True)
    building = models.CharField(max_length=100, blank=True)
    floor = models.CharField(max_length=20, blank=True)
    capacity = models.PositiveIntegerField(default=30)
    has_projector = models.BooleanField(default=False)
    has_ac = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.building}) — cap. {self.capacity}"


# ╔══════════════════════════════════════════════════════════════════════════════════╗
# ║  ──── 7. SKILL TRACKING SYSTEM (Student Feature 3) ───────────────────────────║
# ╚══════════════════════════════════════════════════════════════════════════════════╝

class SkillCourse(models.Model):
    DIFFICULTY_CHOICES = [('beginner', 'Beginner'), ('intermediate', 'Intermediate'),
                          ('advanced', 'Advanced'), ('expert', 'Expert')]
    PLATFORM_CHOICES = [
        ('internal', 'Internal'), ('coursera', 'Coursera'), ('udemy', 'Udemy'),
        ('nptel', 'NPTEL'), ('github', 'GitHub'), ('khan', 'Khan Academy'),
        ('edx', 'edX'), ('other', 'Other'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    platform = models.CharField(max_length=30, choices=PLATFORM_CHOICES, default='internal')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    skill_tags = models.CharField(max_length=300, blank=True, help_text="Comma-separated: e.g. Python, ML, Java")
    icon_url = models.URLField(blank=True, null=True)
    course_url = models.URLField(blank=True)
    external_certificate_url = models.URLField(blank=True, null=True,
                                               help_text="Certificate URL if certificate is issued externally")
    estimated_hours = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f"{self.title} [{self.platform}] — {self.get_difficulty_display()}"


class StudentSkill(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'), ('in_progress', 'In Progress'),
        ('completed', 'Completed'), ('certified', 'Certified'),
    ]
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='student_skills')
    skill_course = models.ForeignKey(SkillCourse, on_delete=models.CASCADE, related_name='enrollments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    progress_percent = models.PositiveIntegerField(default=0, help_text="0-100")
    score = models.FloatField(null=True, blank=True, help_text="Test / quiz score")
    hours_spent = models.FloatField(default=0.0)
    certificate_url = models.URLField(blank=True, null=True)
    certificate_number = models.CharField(max_length=100, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        unique_together = ['student', 'skill_course']

    def __str__(self):
        return f"{self.student.name} — {self.skill_course.title} [{self.status}]"


# ╔══════════════════════════════════════════════════════════════════════════════════╗
# ║  ──── 7-B. GAMIFICATION ───────────────────────────────────────────────────────║
# ╚══════════════════════════════════════════════════════════════════════════════════╝


class Achievement(models.Model):
    """A type of badge/medal a student can earn."""
    ACHIEVEMENT_TYPE_CHOICES = [
        ('attendance', 'Attendance'), ('academic', 'Academic'), ('behavior', 'Behavior'),
        ('streak', 'Streak'), ('special', 'Special'), ('skill', 'Skill'),
    ]
    name = models.CharField(max_length=120, unique=True)
    skill_type = models.CharField(max_length=30, choices=ACHIEVEMENT_TYPE_CHOICES, default='academic')
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, default='fas fa-trophy',
                            help_text="FontAwesome icon class, e.g. 'fas fa-star'")
    xp_reward = models.PositiveIntegerField(default=10)
    threshold = models.CharField(max_length=100, blank=True,
                                 help_text="Human-readable criteria, e.g. '100% attendance for 30 days'")
    criteria = models.JSONField(default=dict, blank=True,
                                help_text="Structured criteria: subject, min_pct, min_streak, etc.")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['xp_reward']

    def __str__(self):
        return f"🏆 {self.name} (+{self.xp_reward} XP)"


class StudentAchievement(models.Model):
    """Junction: awarded achievements per student."""
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='student_achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name='student_awards')
    xp_earned = models.PositiveIntegerField(default=0)
    awarded_at = models.DateTimeField(auto_now_add=True)
    notes = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['-awarded_at']
        unique_together = ['student', 'achievement']

    def __str__(self):
        return f"Award: {self.student.name} → {self.achievement.name} ({self.xp_earned} XP)"


class Leaderboard(models.Model):
    """Periodic leaderboard snapshot (weekly / monthly / term)."""
    SCOPE_CHOICES = [
        ('class', 'Class'), ('section', 'Section'), ('level', 'Education Level'),
        ('subject', 'Subject'), ('overall', 'Overall'),
    ]
    scope = models.CharField(max_length=20, choices=SCOPE_CHOICES)
    target_class = models.CharField(max_length=20, blank=True)
    target_section = models.CharField(max_length=5, blank=True)
    level = models.CharField(max_length=20, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    period_start = models.DateField()
    period_end = models.DateField()
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-generated_at']

    def __str__(self):
        return f"Leaderboard: {self.get_scope_display()} — {self.period_start} → {self.period_end}"


class LeaderboardEntry(models.Model):
    leaderboard = models.ForeignKey(Leaderboard, on_delete=models.CASCADE, related_name='entries')
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='leaderboard_entries')
    rank = models.PositiveIntegerField()
    total_xp = models.PositiveIntegerField(default=0)
    xp_source = models.CharField(max_length=100, blank=True, help_text="e.g. Exams+Participation+Achievements")
    score = models.FloatField(default=0.0, help_text="Primary score used for ranking")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['rank']
        unique_together = ['leaderboard', 'student']

    def __str__(self):
        return f"#{self.rank} {self.student.name} ({self.total_xp} XP)"


class DailyStreak(models.Model):
    """Consecutive-day learning activity tracker."""
    student = models.OneToOneField('Student', on_delete=models.CASCADE, related_name='daily_streak')
    current_streak = models.PositiveIntegerField(default=0, help_text="Consecutive days with activity ")
    longest_streak = models.PositiveIntegerField(default=0)
    last_active_date = models.DateField(null=True, blank=True)
    streak_reward_claimed = models.BooleanField(default=False, help_text="Daily reward already given?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-current_streak']

    def __str__(self):
        return f"Streak: {self.student.name} — 🔥 {self.current_streak} days"


# ╔══════════════════════════════════════════════════════════════════════════════════╗
# ║  ──── 8. STUDENT COLLABORATION TOOLS (Student Features 1 & 6) ─────────────────║
# ╚══════════════════════════════════════════════════════════════════════════════════╝

class StudyGroup(models.Model):
    STATUS_CHOICES = [('active', 'Active'), ('archived', 'Archived')]
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    target_class = models.CharField(max_length=20, blank=True)
    created_by = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='created_study_groups')
    members = models.ManyToManyField('Student', related_name='joined_study_groups', blank=True)
    max_members = models.PositiveIntegerField(default=20)
    is_private = models.BooleanField(default=False, help_text="Invite‑only group")
    invite_code = models.CharField(max_length=12, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"StudyGroup: {self.name} — {self.members.count()} members"


class StudyGroupMessage(models.Model):
    study_group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, related_name='group_messages')
    sender = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='group_messages_sent')
    message = models.TextField()
    attachment = models.FileField(upload_to='study_group_attachments/', null=True, blank=True)
    is_read = models.BooleanField(default=False)
    read_by = models.ManyToManyField('Student', related_name='read_group_messages', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Msg: {self.sender.name} → {self.study_group.name} @ {self.created_at.strftime('%H:%M')}"


class SharedNote(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    owner = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='shared_notes_owned')
    study_group = models.ForeignKey(StudyGroup, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='shared_notes')
    co_editors = models.ManyToManyField('Student', related_name='editable_shared_notes', blank=True)
    viewers = models.ManyToManyField('Student', related_name='viewable_shared_notes', blank=True)
    tags = models.CharField(max_length=200, blank=True, help_text="Comma‑separated")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"Note: {self.title} — by {self.owner.name}"


# ╔══════════════════════════════════════════════════════════════════════════════════╗
# ║  ──── 10. STUDENT GOALS ───────────────────────────────────────────────────────║
# ╚══════════════════════════════════════════════════════════════════════════════════╝


class StudentGoal(models.Model):
    STATUS_CHOICES = [('active', 'Active'), ('completed', 'Completed'), ('cancelled', 'Cancelled')]
    PRIORITY_CHOICES = [('low', 'Low'), ('medium', 'Medium'), ('high', 'High')]
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='goals')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    target_marks = models.FloatField(null=True, blank=True, help_text="Target end score")
    current_progress = models.FloatField(default=0.0, help_text="0-100")
    deadline = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='active')
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['priority', '-deadline', '-created_at']

    def __str__(self):
        return f"Goal: {self.student.name} — {self.title} ({self.current_progress}%)"


# ╔══════════════════════════════════════════════════════════════════════════════════╗
# ║  ──── 6 & 10. DIGITAL ID CARD & ONLINE LEARNING PORTAL ───────────────────────║
# ╚══════════════════════════════════════════════════════════════════════════════════╝

class StudentIDCard(models.Model):
    student = models.OneToOneField('Student', on_delete=models.CASCADE, related_name='digital_id_card')
    card_number = models.CharField(max_length=50, unique=True)
    qr_data = models.CharField(max_length=512, help_text="JSON info encoded in QR for verification")
    qr_image = models.ImageField(upload_to='student_id_qr/', null=True, blank=True)
    issued_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['card_number']

    def __str__(self):
        return f"ID Card: {self.student.name} — {self.card_number}"


class VideoLecture(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='video_lectures')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='video_lectures')
    target_class = models.CharField(max_length=20)
    target_section = models.CharField(max_length=5, default='')
    video_file = models.FileField(upload_to='video_lectures/', null=True, blank=True)
    video_url = models.URLField(blank=True, help_text="YouTube / Vimeo embed or stream link")
    duration_minutes = models.PositiveIntegerField(default=0)
    thumbnail_url = models.URLField(blank=True, null=True)
    chapter = models.CharField(max_length=100, blank=True)
    is_published = models.BooleanField(default=False)
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Video: {self.title} — {self.subject.name}"


# ╔══════════════════════════════════════════════════════════════════════════════════╗
# ║  ──── 10-B. CAREER & INTERNSHIP PORTAL ──────────────────────────────────────║
# ╚══════════════════════════════════════════════════════════════════════════════════╝

JOB_TYPE_CHOICES = [
    ('internship', 'Internship'), ('full_time', 'Full-Time'), ('part_time', 'Part-Time'),
    ('freelance', 'Freelance'), ('apprenticeship', 'Apprenticeship'),
]


class CareerPortalListing(models.Model):
    STAGE_CHOICES = [('open', 'Applications Open'), ('closed', 'Closed'), ('hired', 'Positions Filled')]
    title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    company_logo_url = models.URLField(blank=True, null=True)
    description = models.TextField()
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    location = models.CharField(max_length=200, blank=True)
    salary_range = models.CharField(max_length=100, blank=True)
    required_skills = models.TextField(blank=True)
    posted_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    application_url = models.URLField(blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    stage = models.CharField(max_length=15, choices=STAGE_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-deadline', '-created_at']

    def __str__(self):
        return f"{self.title} @ {self.company_name}"


class StudentApplication(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'), ('shortlisted', 'Shortlisted'), ('interview', 'Interview Scheduled'),
        ('selected', 'Selected'), ('rejected', 'Rejected'), ('withdrawn', 'Withdrawn'),
    ]
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='applications')
    listing = models.ForeignKey(CareerPortalListing, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField(blank=True)
    resume_url = models.URLField(blank=True)
    transcript = models.FileField(upload_to='student_applications/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    notes = models.TextField(blank=True, help_text="Recruiter / college notes")
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-applied_at']
        unique_together = ['student', 'listing']

    def __str__(self):
        return f"{self.student.name} → {self.listing.title} [{self.status}]"


# ╔══════════════════════════════════════════════════════════════════════════════════╗
# ║  ──── 10-C. AI TEACHING ASSISTANT ───────────────────────────────────────────║
# ╚══════════════════════════════════════════════════════════════════════════════════╝

class AIQuiz(models.Model):
    """AI-generated quiz for any subject/topic."""
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='ai_generated_quizzes')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='ai_quizzes')
    title = models.CharField(max_length=200)
    class_section = models.CharField(max_length=20)
    topic_prompt = models.TextField(help_text="Topic / chapter the AI should generate questions about")
    number_of_questions = models.PositiveIntegerField(default=10)
    difficulty_distribution = models.JSONField(default=dict, blank=True,
                                               help_text="{\"easy\": 30, \"medium\": 50, \"hard\": 20}")
    generating_model = models.CharField(max_length=50, default='AI-Engine-v1',
                                        help_text="Version / name of the AI engine used")
    generated_questions = models.JSONField(default=list, blank=True, help_text="Raw AI output stored as JSON")
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"AI Quiz: {self.title} — {self.subject.name} ({self.get_publish_status_display()})"


class AILessonPlan(models.Model):
    """AI-generated lesson plan."""
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='ai_lesson_plans')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='ai_lesson_plans')
    class_section = models.CharField(max_length=20)
    chapter_topic = models.CharField(max_length=200)
    duration_minutes = models.PositiveIntegerField(default=45)
    teaching_method = models.CharField(max_length=50, choices=TEACHING_METHOD_CHOICES,
                                       default='lecture')
    generated_content = models.TextField(help_text="Full lesson plan text from AI")
    learning_outcomes = models.TextField(blank=True)
    quiz_suggestions = models.TextField(blank=True, help_text="AI‑suggested quiz questions")
    is_applied = models.BooleanField(default=False, help_text="Has teacher applied this plan?")
    applied_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"AI Plan: {self.chapter_topic} — {self.subject.name} ({self.class_section})"


# ╔══════════════════════════════════════════════════════════════════════════════════╗
# ║  ──── 7-C. PARENT PORTAL ─────────────────────────────────────────────────────║
# ╚══════════════════════════════════════════════════════════════════════════════════╝

class ParentNotification(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='portal_notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=[
        ('info', 'Info'), ('warning', 'Warning'), ('urgent', 'Urgent'), ('fee_due', 'Fee Due'),
    ])
    is_read = models.BooleanField(default=False)
    link_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"PN: {self.parent.guardian_name or self.parent.father_name} — {self.title}"


class ParentMeeting(models.Model):
    STATUS_CHOICES = [('requested', 'Requested'), ('confirmed', 'Confirmed'),
                      ('completed', 'Completed'), ('cancelled', 'Cancelled')]
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='meetings')
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='parent_meetings')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='parent_meetings')
    requested_at = models.DateTimeField(auto_now_add=True)
    preferred_date = models.DateField()
    preferred_time = models.TimeField(null=True, blank=True)
    confirmed_date = models.DateField(null=True, blank=True)
    confirmed_time = models.TimeField(null=True, blank=True)
    agenda = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
    meeting_link = models.URLField(blank=True, null=True, help_text="Video call link")

    class Meta:
        ordering = ['-preferred_date']

    def __str__(self):
        return f"Meeting: {self.parent.guardian_name or self.parent.father_name} × {self.teacher.get_full_name()}"


# ╔══════════════════════════════════════════════════════════════════════════════════╗
# ║  ──── 7-D. TRANSPORT & HOSTEL ────────────────────────────────────────────────║
# ╚══════════════════════════════════════════════════════════════════════════════════╝


class BusRoute(models.Model):
    name = models.CharField(max_length=100, unique=True)
    driver_name = models.CharField(max_length=100, blank=True)
    driver_phone = models.CharField(max_length=20, blank=True)
    bus_number = models.CharField(max_length=30, blank=True)
    capacity = models.PositiveIntegerField(default=30)
    is_active = models.BooleanField(default=True)
    tracking_device_id = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} [{self.bus_number}] — {self.driver_name}"


class BusStop(models.Model):
    route = models.ForeignKey(BusRoute, on_delete=models.CASCADE, related_name='stops')
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    estimated_arrival = models.TimeField(null=True, blank=True)
    stop_order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['route', 'stop_order']
        unique_together = ['route', 'stop_order']

    def __str__(self):
        return f"{self.route.name} — Stop {self.stop_order}: {self.name}"


class StudentTransportCard(models.Model):
    student = models.OneToOneField('Student', on_delete=models.CASCADE, related_name='transport_card')
    card_number = models.CharField(max_length=50, unique=True)
    qr_code = models.ImageField(upload_to='transport_qr/', null=True, blank=True)
    route = models.ForeignKey(BusRoute, on_delete=models.SET_NULL, null=True, blank=True)
    bus_stop = models.ForeignKey(BusStop, on_delete=models.SET_NULL, null=True, blank=True)
    issued_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    last_swipe = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['card_number']

    def __str__(self):
        return f"Transport Card: {self.student.name} — {self.card_number}"


class TransportMonitor(models.Model):
    route = models.ForeignKey(BusRoute, on_delete=models.CASCADE, related_name='monitor_entries')
    student = models.ForeignKey('Student', on_delete=models.CASCADE, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    speed_km_h = models.FloatField(null=True, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-recorded_at']

    def __str__(self):
        return f"Bus Track: {self.route.name} — {self.recorded_at.strftime('%Y-%m-%d %H:%M')}"


class HostelRoom(models.Model):
    room_number = models.CharField(max_length=20, unique=True)
    building = models.CharField(max_length=50, blank=True)
    capacity = models.PositiveIntegerField(default=2)
    current_occupants = models.PositiveIntegerField(default=0)
    floor = models.CharField(max_length=10, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['building', 'room_number']

    def __str__(self):
        return f"Room {self.room_number} ({self.building})"


class HostelAllocation(models.Model):
    STATUS_CHOICES = [
        ('occupied', 'Occupied'), ('vacated', 'Vacated'), ('pending', 'Pending'), ('maintenance', 'Maintenance'),
    ]
    room = models.ForeignKey(HostelRoom, on_delete=models.CASCADE, related_name='allocations')
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='hostel_allocations')
    allocated_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    allocation_date = models.DateField(auto_now_add=True)
    vacate_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='occupied')
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-allocation_date']
        unique_together = ['room', 'status']

    def __str__(self):
        return f"Hostel: {self.student.name} → {self.room.room_number}"


# ╔══════════════════════════════════════════════════════════════════════════════════╗
# ║  ──── 8-B. AI RECOMMENDATION ENGINE ──────────────────────────────────────────║
# ╚══════════════════════════════════════════════════════════════════════════════════╝


class AIRecommendation(models.Model):
    REC_TYPE_CHOICES = [
        ('career_skill', 'Career / Skill Suggestion'), ('improvement', 'Subject Improvement'),
        ('note', 'Note / Resource'), ('course', 'Course / Paper Suggestion'),
        ('scholarship', 'Scholarship'), ('exam', 'Exam Focus Area'),
    ]
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='ai_recommendations')
    recommendation_type = models.CharField(max_length=30, choices=REC_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    detail = models.TextField(help_text="Full AI-generated recommendation text")
    generated_by = models.CharField(max_length=50, default='AI-Engine-v1')
    confidence = models.FloatField(default=0.0, help_text="0–1 confidence in recommendation quality")
    is_read = models.BooleanField(default=False)
    priority = models.CharField(max_length=10, choices=[
        ('low', 'Low'), ('medium', 'Medium'), ('high', 'High'),
    ], default='medium')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at', '-priority']

    def __str__(self):
        return f"Rec: {self.student.name} — {self.title} [{self.get_recommendation_type_display()}]"


class AIStudentReport(models.Model):
    """Yearly / term‑wise per‑student AI analytics report."""
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='ai_reports')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.SET_NULL, null=True)
    academic_risk = models.CharField(max_length=20, default='low', choices=[
        ('low', 'Low'), ('medium', 'Medium'), ('high', 'High'),
    ])
    behavior_risk = models.CharField(max_length=20, default='low', choices=[
        ('low', 'Low'), ('medium', 'Medium'), ('high', 'High'),
    ])
    attendance_risk = models.CharField(max_length=20, default='low', choices=[
        ('low', 'Low'), ('medium', 'Medium'), ('high', 'High'),
    ])
    attendance_percentage = models.FloatField(default=0.0)
    risk_score = models.FloatField(default=0.0, help_text="0 = safe, 100 = at‑risk")
    recommendations = models.JSONField(default=dict, blank=True,
                                       help_text="AI-generated {risk_area: [recommendation strings]}")
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-academic_year__start_date', 'student__name']
        verbose_name = 'AI Student Report'

    def __str__(self):
        yr = self.academic_year.name if self.academic_year else '—'
        return f"AI Report: {self.student.name} — {yr}"


# ╔══════════════════════════════════════════════════════════════════════════════════╗
# ║  ──── NEXT-LEVEL: AI Voice, Multi-College, Smart Campus ───────────────────────║
# ╚══════════════════════════════════════════════════════════════════════════════════╝


class MultilingualVoiceSession(models.Model):
    LANGUAGE_CHOICES = [('en', 'English'), ('ne', 'Nepali'), ('hi', 'Hindi'), ('mixed', 'Mixed')]
    STATUS_CHOICES = [('active', 'Active'), ('ended', 'Ended'), ('failed', 'Failed')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='voice_sessions')
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='en')
    transcript = models.TextField(blank=True, help_text="Speech-to-text transcript")
    intent = models.CharField(max_length=100, blank=True, help_text="Detected user intent")
    resolved = models.BooleanField(default=False)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='active')
    duration_seconds = models.PositiveIntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f"Voice: {self.user.username} [{self.language}] {self.started_at.strftime('%Y-%m-%d %H:%M')}"


class IoTDevice(models.Model):
    DEVICE_TYPE_CHOICES = [
        ('projector', 'Projector'), ('light', 'Smart Light'), ('ac', 'Air Conditioner'),
        ('camera', 'Security Camera'), ('sensor', 'Environmental Sensor'),
        ('door', 'Smart Door Lock'), ('other', 'Other'),
    ]
    name = models.CharField(max_length=150)
    device_type = models.CharField(max_length=30, choices=DEVICE_TYPE_CHOICES)
    classroom = models.CharField(max_length=100, blank=True)
    location_description = models.CharField(max_length=200, blank=True)
    device_id = models.CharField(max_length=100, unique=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    mac_address = models.CharField(max_length=50, blank=True)
    is_on = models.BooleanField(default=False)
    last_ping = models.DateTimeField(null=True, blank=True)
    is_online = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['classroom', 'name']

    def __str__(self):
        return f"{self.device_type.title()}: {self.name} [{self.classroom}]"


class SmartEnergyLog(models.Model):
    classroom = models.CharField(max_length=100, blank=True)
    device = models.ForeignKey(IoTDevice, on_delete=models.CASCADE, null=True, blank=True, related_name='energy_logs')
    power_consumption_kw = models.FloatField(default=0.0)
    voltage = models.FloatField(null=True, blank=True)
    current_a = models.FloatField(null=True, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-recorded_at']

    def __str__(self):
        return f"Energy: {self.classroom or self.device} — {self.recorded_at.strftime('%Y-%m-%d %H:%M')}"


class Institution(models.Model):
    """Multi-college / multi-school support — each record is one college or school."""
    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=30, unique=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default='Nepal')
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=30, blank=True)
    website = models.URLField(blank=True)
    logo_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} [{self.code}]"


class InstitutionUser(models.Model):
    """Links a Django user to an institution (for multi-instance setups)."""
    ROLE_CHOICES = [('owner', 'Owner / Super Admin'), ('admin', 'Admin'), ('teacher', 'Teacher'),
                    ('student', 'Student'), ('parent', 'Parent'), ('viewer', 'Viewer')]
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='users')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='institution_users')
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='student')
    linked_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['institution', 'user']
        ordering = ['institution', 'role']

    def __str__(self):
        return f"{self.user.username} → {self.institution.name} [{self.role}]"

