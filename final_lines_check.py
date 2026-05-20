"""Show what the final 60 lines of the template look like with indents."""
with open(r'core/templates/core/dashboard/upload_marks_excel.html', encoding='utf-8') as f:
    lines = f.readlines()

with open('final_60_lines.txt', 'w', encoding='utf-8') as out:
    out.write("=== Last 60 lines of upload_marks_excel.html ===\n")
    start = max(0, len(lines) - 60)
    for i, line in enumerate(lines[start:], start=start+1):
        leading = len(line) - len(line.lstrip())
        stripped = line.strip()
        tag = ""
        if stripped.startswith('<div'):
            tag = "DIV_OPEN"
        elif stripped == '</div>':
            tag = "DIV_CLOSE"
        elif stripped.startswith('<form'):
            tag = "FORM_OPEN"
        elif stripped == '</form>':
            tag = "FORM_CLOSE"
        out.write(f"{i:4d}  [{leading:2d}]  {tag:<10}  {repr(stripped[:80])}\n")
