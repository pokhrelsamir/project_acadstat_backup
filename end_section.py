"""Check if toast and flex divs are actually closed later in the file."""
with open(r'core/templates/core/dashboard/upload_marks_excel.html', encoding='utf-8') as f:
    lines = f.readlines()

# Show div opens/closes from line 880 onwards
print("Last 60 lines:")
for i, line in enumerate(lines[804:], start=805):
    stripped = line.strip()
    if not stripped:
        print(f"{i:4d}: (empty)")
        continue
    if '<div' in stripped:
        print(f"{i:4d}: DIV_OPEN  {repr(stripped[:70])}")
    if '</div>' in stripped:
        print(f"{i:4d}: DIV_CLOSE {repr(stripped[:70])}")
    if '</form>' in stripped:
        print(f"{i:4d}: FORM_END  {repr(stripped[:70])}")
    if '<form' in stripped:
        print(f"{i:4d}: FORM_OPEN {repr(stripped[:70])}")
