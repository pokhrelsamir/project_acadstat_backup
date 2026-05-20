# -*- coding: utf-8 -*-
"""Append T8/T9/T10/A12 views to core/views.py"""

BLOCK = '''

# %% T8 SMART QUESTION BANK %%
@teacher_required
def question_bank(request):
    from core.models import QuestionBank, QUESTION_TYPE_CHOICES, DIFFICULTY_CHOICES
    qs = QuestionBank.objects.filter(teacher=request.teacher).select_related("subject")
    subject_id   = request.GET.get("subject", "").strip()
    chapter      = request.GET.get("chapter", "").strip()
    difficulty   = request.GET.get("difficulty", "").strip()
    qtype        = request.GET.get("type", "").strip()
    if subject_id:   qs = qs.filter(subject_id=subject_id)
    if chapter:      qs = qs.filter(chapter__icontains=chapter)
    if difficulty:   qs = qs.filter(difficulty=difficulty)
    if qtype:        qs = qs.filter(question_type=qtype)

    if request.GET.get("export") == "csv":
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=question_bank.csv"
        writer = csv.writer(response)
        writer.writerow(["Subject", "Type", "Question", "Options", "Correct", "Difficulty", "Chapter", "Marks"])
        for q in qs:
            opts = "; ".join(f"{o.get("key","")}: {o.get("text","")}" for o in (q.options or []))
            writer.writerow([q.subject.code, q.get_question_type_display(), q.question_text,
                             opts, q.correct_answer, q.get_difficulty_display(), q.chapter, q.marks])
        return response

    subjects = request.teacher.subjects.all()
    chapters = sorted(set(QuestionBank.objects.filter(teacher=request.teacher)
                         .values_list("chapter", flat=True).exclude(chapter="")))

    context = {
        "questions": qs, "subjects": subjects, "chapters": chapters,
        "difficulties": DIFFICULTY_CHOICES, "qtypes": QUESTION_TYPE_CHOICES,
        "filter_subject": subject_id, "filter_chapter": chapter,
        "filter_difficulty": difficulty, "filter_type": qtype,
    }
    return render(request, "core/dashboard/question_bank.html", context)


@teacher_required
def question_bank_add(request, qid=None):
    from core.models import QuestionBank, QUESTION_TYPE_CHOICES, DIFFICULTY_CHOICES
    question = None
    if qid:
        question = get_object_or_404(QuestionBank, id=qid, teacher=request.teacher)

    if request.method == "POST":
        subject_id     = request.POST.get("subject")
        question_text  = request.POST.get("question_text", "").strip()
        question_type  = request.POST.get("question_type", "")
        options_raw    = request.POST.get("options_json", "[]")
        correct_answer = request.POST.get("correct_answer", "").strip()
        difficulty     = request.POST.get("difficulty", "medium")
        chapter        = request.POST.get("chapter", "").strip()
        marks          = int(request.POST.get("marks") or 1)
        tags           = request.POST.get("tags", "").strip()
        try:
            options = json.loads(options_raw)
        except (json.JSONDecodeError, ValueError):
            options = question.options if question else []

        if qid:
            subject = get_object_or_404(Subject, id=subject_id)
            question.subject_id = subject.id
            question.question_text = question_text
            question.question_type = question_type
            question.options = options
            question.correct_answer = correct_answer
            question.difficulty = difficulty
            question.chapter = chapter
            question.marks = marks
            question.tags = tags
            question.save()
            messages.success(request, "Question updated successfully.")
        else:
            subject = get_object_or_404(Subject, id=subject_id)
            QuestionBank.objects.create(
                teacher=request.teacher, subject=subject,
                question_text=question_text, question_type=question_type,
                options=options, correct_answer=correct_answer,
                difficulty=difficulty, chapter=chapter, marks=marks, tags=tags,
            )
            messages.success(request, "Question added successfully.")
        return redirect("core:question_bank")

    subjects = request.teacher.subjects.all()
    ctx = {
        "question": question, "subjects": subjects,
        "qtypes": QUESTION_TYPE_CHOICES, "difficulties": DIFFICULTY_CHOICES,
        "options_json": json.dumps(question.options or []) if question else "[]",
    }

    return render(request, "core/dashboard/question_bank_add.html", ctx)


def _qb_question_bank_add(request):
    """Add a single question — wraps question_bank_add without qid"""
    return question_bank_add(request, qid=None)


def _qb_question_bank_edit(request, qid):
    """Edit a single question — wraps question_bank_add with qid"""
    return question_bank_add(request, qid=qid)


@teacher_required
def question_bank_delete(request, qid):
    question = get_object_or_404(QuestionBank, id=qid, teacher=request.teacher)
    question.delete()
    messages.success(request, "Question deleted successfully.")
    return redirect("core:question_bank")


@teacher_required
def question_bank_import(request):
    from core.models import QuestionBank
    if request.method == "POST":
        uploaded = request.FILES.get("file")
        if not uploaded:
            messages.error(request, "Please select a file.")
            return redirect("core:question_bank_import")

        try:
            data = json.loads(uploaded.read().decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            try:
                data = json.loads(uploaded.read().decode("latin-1", errors="replace"))
            except json.JSONDecodeError:
                messages.error(request, "Invalid file format. Upload a valid JSON file.")
                return redirect("core:question_bank_import")

        if not isinstance(data, list):
            messages.error(request, "JSON root must be an array of question objects.")
            return redirect("core:question_bank_import")

        created = 0
        for item in data:
            subj_code = item.get("subject") or item.get("subject_code")
            subj = Subject.objects.filter(code=subj_code).first() if subj_code else None
            if not subj or not request.teacher.subjects.filter(id=subj.id).exists():
                continue
            QuestionBank.objects.update_or_create(
                subject=subj,
                question_text=item.get("question_text", "").strip(),
                defaults={
                    "teacher": request.teacher,
                    "question_type": item.get("question_type", "short_answer"),
                    "options": item.get("options", []),
                    "correct_answer": item.get("correct_answer", ""),
                    "difficulty": item.get("difficulty", "medium"),
                    "chapter": item.get("chapter", ""),
                    "marks": int(item.get("marks", 1)),
                    "tags": item.get("tags", ""),
                },
            )
            created += 1
        messages.success(request, f"{created} questions imported successfully.")
        return redirect("core:question_bank")

    return render(request, "core/dashboard/question_bank_import.html")


# ── T8. PAPER TEMPLATE ──────────────────────────────────────────────────────────

@teacher_required
def paper_template_list(request):
    from core.models import QuestionPaperTemplate
    templates = QuestionPaperTemplate.objects.filter(teacher=request.teacher).select_related("subject")
    return render(request, "core/dashboard/paper_template_list.html", {"templates": templates})


@teacher_required
def paper_template_create(request):
    from core.models import QuestionPaperTemplate as QPT
    if request.method == "POST":
        name             = request.POST.get("name", "").strip()
        subject_id       = request.POST.get("subject")
        total_marks      = int(request.POST.get("total_marks") or 100)
        duration_minutes = int(request.POST.get("duration_minutes") or 90)
        try:
            distribution = json.loads(request.POST.get("distribution_json", "{}"))
        except (ValueError, json.JSONDecodeError):
            distribution = {}
        try:
            chapters = json.loads(request.POST.get("chapters_json", "[]"))
        except (ValueError, json.JSONDecodeError):
            chapters = []
        subject = get_object_or_404(Subject, id=subject_id)
        QPT.objects.create(
            name=name, subject=subject, total_marks=total_marks,
            duration_minutes=duration_minutes, distribution=distribution,
            chapters=chapters, teacher=request.teacher,
        )
        messages.success(request, "Paper template created.")
        return redirect("core:paper_template_list")

    subjects = request.teacher.subjects.all()
    return render(request, "core/dashboard/paper_template_create.html", {"subjects": subjects})


@teacher_required
def paper_template_generate(request, tid):
    from core.models import QuestionPaperTemplate as QPT
    template = get_object_or_404(QPT, id=tid, teacher=request.teacher)
    dist = template.distribution or {}
    qs = QuestionBank.objects.filter(
        teacher=request.teacher, subject=template.subject, difficulty__in=["easy", "medium", "hard"]
    )
    if template.chapters:
        qs = qs.filter(chapter__in=template.chapters)
    selected = []
    for diff, cnt in dist.items():
        selected.extend(list(qs.filter(difficulty=diff)[:int(cnt)]))
    total_marks = sum(q.marks for q in selected)
    return render(request, "core/dashboard/paper_template_generate.html", {
        "template": template, "questions": selected, "total_marks": total_marks,
    })


# %% T9 REMINDER SCHEDULER %%
@teacher_required
def reminder_list(request):
    from core.models import Reminder
    reminders = Reminder.objects.filter(teacher=request.teacher).select_related("student", "subject")
    return render(request, "core/dashboard/reminder_list.html", {"reminders": reminders})


@teacher_required
def reminder_create(request):
    from core.models import Reminder, REMINDER_TYPE_CHOICES, RECURRENCE_CHOICES
    if request.method == "POST":
        reminder_type    = request.POST.get("reminder_type", "")
        student_id       = request.POST.get("student", "").strip()
        subject_id       = request.POST.get("subject", "").strip()
        title            = request.POST.get("title", "").strip()
        message          = request.POST.get("message", "").strip()
        scheduled_for    = request.POST.get("scheduled_for", "").strip()
        recurrence       = request.POST.get("recurrence", "none")
        recurrence_until = request.POST.get("recurrence_until", "").strip()
        student = Student.objects.filter(id=student_id).first() if student_id else None
        subject = Subject.objects.filter(id=subject_id).first() if subject_id else None
        ru_date = None
        if recurrence_until:
            try:
                ru_date = datetime.strptime(recurrence_until, "%Y-%m-%d").date()
            except ValueError:
                pass
        Reminder.objects.create(
            teacher=request.teacher, student=student, subject=subject,
            reminder_type=reminder_type, title=title, message=message,
            scheduled_for=scheduled_for, recurrence=recurrence,
            recurrence_until=ru_date,
        )
        messages.success(request, "Reminder created.")
        return redirect("core:reminder_list")

    subjects = request.teacher.subjects.all()
    students = request.teacher.students.all().order_by("name")
    return render(request, "core/dashboard/reminder_create.html", {
        "subjects": subjects, "students": students,
        "rtypes": REMINDER_TYPE_CHOICES, "recurrences": RECURRENCE_CHOICES,
    })


@teacher_required
@require_http_methods(["POST"])
def reminder_delete(request, reminder_id):
    reminder = get_object_or_404(Reminder, id=reminder_id, teacher=request.teacher)
    reminder.delete()
    messages.success(request, "Reminder deleted.")
    return redirect("core:reminder_list")


@_admin_required
def scheduled_tasks_list(request):
    from core.models import ScheduledTask, SCHEDULED_TASK_TYPE_CHOICES
    tasks = ScheduledTask.objects.all().order_by("-scheduled_for")[:200]
    return render(request, "core/dashboard/scheduled_tasks_list.html", {
        "tasks": tasks, "task_types": SCHEDULED_TASK_TYPE_CHOICES,
    })


# %% T10 SMART SUBJECT ANALYSIS %%
@teacher_required
def subject_analytics(request):
    from core.models import QuestionBank, QuestionPaperTemplate
    teacher         = request.teacher
    subject_id      = request.GET.get("subject", "").strip()
    terminal        = request.GET.get("terminal", "all")

    teacher_subjects = teacher.subjects.all()
    teacher_students = teacher.students.all()
    all_subjects = teacher_subjects.order_by("name")

    base_qs = Result.objects.filter(
        student__in=teacher_students, subject__in=all_subjects
    ).select_related("student", "subject")
    if subject_id:
        base_qs = base_qs.filter(subject_id=subject_id)

    bins_labels = ["0-39", "40-49", "50-59", "60-69", "70-79", "80-89", "90-100"]
    bins = [0] * 7
    pct_list = []
    for r in base_qs:
        pct = (r.marks_obtained / r.total_marks * 100) if r.total_marks > 0 else 0
        pct_list.append(pct)
        if pct < 40:    bins[0] += 1
        elif pct < 50:  bins[1] += 1
        elif pct < 60:  bins[2] += 1
        elif pct < 70:  bins[3] += 1
        elif pct < 80:  bins[4] += 1
        elif pct < 90:  bins[5] += 1
        else:           bins[6] += 1

    total       = len(pct_list)
    avg_pct     = round(sum(pct_list) / total, 1) if total else 0
    highest_pct = round(max(pct_list), 1) if pct_list else 0
    lowest_pct  = round(min(pct_list), 1) if pct_list else 0
    pass_count  = sum(1 for p in pct_list if p >= 40)
    pass_rate   = round((pass_count / total) * 100, 1) if total else 0
    below_40    = sum(1 for p in pct_list if p < 40)

    insight_lines = []
    if below_40 > 0:
        s = "s" if below_40 > 1 else ""
        insight_lines.append(f"Warning: {below_40} student{s} scored below 40% — consider arranging a remedial class or revision session.")
    if avg_pct >= 80:
        insight_lines.append(f"Excellent! Class average is {avg_pct}%.")
    elif avg_pct >= 70:
        insight_lines.append(f"Good progress — class average is {avg_pct}%.")
    elif avg_pct >= 50:
        insight_lines.append(f"Class average is {avg_pct}%. Focus on weaker students.")
    else:
        insight_lines.append(f"Class average is {avg_pct}%. Needs urgent attention.")

    terminals = ["1st", "2nd", "3rd", "Final"]
    run_terminals = terminals if terminal == "all" else [terminal]

    trender = {}
    student_result_qs = base_qs.order_by("student__name", "terminal")
    for r in student_result_qs:
        sid = r.student.id
        if sid not in trender:
            trender[sid] = {"student": r.student, "marks_by_term": {}}
        trender[sid]["marks_by_term"][r.terminal] = r.marks_obtained

    trend_rows = []
    for sid in sorted(trender, key=lambda s: trender[s]["student"].name):
        info = trender[sid]
        student = info["student"]
        mbt = info["marks_by_term"]
        prev_vals = [mbt.get(t) for t in terminals[:-1]]
        if len(prev_vals) >= 2 and prev_vals[-1] is not None and prev_vals[-2] is not None:
            diff = prev_vals[-1] - prev_vals[-2]
            arrow = "up" if diff > 0.5 else ("down" if diff < -0.5 else "same")
        else:
            arrow = "same"
        trend_rows.append({"student": student, "marks": mbt, "arrow": arrow})

    available_classes = sorted(set(s.student_class for s in teacher_students))

    return render(request, "core/dashboard/subject_analytics.html", {
        "subject_obj": Subject.objects.filter(id=subject_id).first(),
        "subject_id": subject_id, "terminal": terminal,
        "running_terminals": run_terminals,
        "total": total, "avg_pct": avg_pct, "highest_pct": highest_pct,
        "lowest_pct": lowest_pct, "pass_rate": pass_rate,
        "pass_count": pass_count, "below_40": below_40,
        "bins_labels": bins_labels, "bins": bins,
        "trend_rows": trend_rows, "insight_lines": insight_lines,
        "available_subjects": all_subjects, "available_classes": available_classes,
        "terminals": terminals, "is_teacher": True,
    })


# %% A12 AUTOMATED DIGESTS (admin-triggered) %%
@_admin_required
def trigger_weekly_digest(request):
    from core.models import ScheduledTask
    from datetime import timedelta
    now  = timezone.now()
    count = 0
    for student in Student.objects.all():
        ScheduledTask.objects.create(
            task_type="sms_digest",
            scheduled_for=now + timedelta(minutes=count),
            payload={"student_id": student.id, "type": "weekly_attendance"},
        )
        count += 1
    messages.success(request, f"Queued {count} weekly attendance digest tasks.")
    return redirect("core:scheduled_tasks_list")


@_admin_required
def trigger_monthly_report(request):
    from core.models import ScheduledTask
    from datetime import timedelta
    now  = timezone.now()
    count = 0
    for student in Student.objects.all():
        ScheduledTask.objects.create(
            task_type="sms_digest",
            scheduled_for=now + timedelta(minutes=count),
            payload={"student_id": student.id, "type": "monthly_report"},
        )
        count += 1
    messages.success(request, f"Queued {count} monthly report tasks.")
    return redirect("core:scheduled_tasks_list")
'''

import os
target = r"C:\Users\poksa\Desktop\abc\core\views.py"
with open(target, "a", encoding="utf-8") as fh:
    fh.write(BLOCK)
print("Done:", target)
