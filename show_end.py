with open(r'core\templates\core\dashboard\upload_marks_excel.html', encoding='utf-8') as f:
    lines = f.readlines()
print(f"Total lines: {len(lines)}")
# Show lines 810 onwards
for i, line in enumerate(lines[810:], start=811):
    print(f"{i:4d}: {repr(line)[:120]}")
