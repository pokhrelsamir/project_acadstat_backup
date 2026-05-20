with open(r'core/templates/core/dashboard/upload_marks_excel.html', encoding='utf-8') as f:
    lines = f.readlines()

with open("html_structure_context.txt", "w", encoding="utf-8") as out:
    out.write("=== Lines 509-520 (form and first form-group) ===\n")
    for i, line in enumerate(lines[508:520], start=509):
        out.write(f"{i:4d}: {line}")
    
    out.write("\n=== Lines 565-595 (labels, form-actions, closing form, instructions open) ===\n")
    for i, line in enumerate(lines[564:595], start=565):
        out.write(f"{i:4d}: {line}")
        
    out.write("\n=== Lines 660-680 (close instructions, close form-card) ===\n")
    for i, line in enumerate(lines[659:680], start=660):
        out.write(f"{i:4d}: {line}")
    
    out.write("\n=== Lines 510-676 (FULL SECTION: form to form-card close) ===\n")
    for i, line in enumerate(lines[509:676], start=510):
        out.write(f"{i:4d}: {line}")
