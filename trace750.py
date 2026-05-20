with open(r'core\templates\core\dashboard\upload_marks_excel.html', encoding='utf-8') as f:
    lines = f.readlines()

# Show lines 750-865
for i, line in enumerate(lines[749:865], start=750):
    print(f"{i:4d}: {repr(line)}")
