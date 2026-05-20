"""Check div nesting context in lines 460-676 (the core layout area)."""
with open(r'core/templates/core/dashboard/upload_marks_excel.html', encoding='utf-8') as f:
    lines = f.readlines()

print("=== DIV OPEN/CLOSE CONTEXT (lines 460-676) ===")
for i, line in enumerate(lines[459:676], start=460):
    stripped = line.strip()
    if not stripped:
        print(f"{i:4d}: (empty)")
        continue
    if '<div' in line.lower() and '>' in line:
        print(f"{i:4d}: <div ...>       {repr(stripped[:70])}")
    elif '</div>' in line.lower():
        print(f"{i:4d}: </div>          {repr(stripped[:70])}")
