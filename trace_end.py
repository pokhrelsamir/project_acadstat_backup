with open(r'core\templates\core\dashboard\upload_marks_excel.html', encoding='utf-8') as f:
    lines = f.readlines()
print("Lines 840-865:")
for i, line in enumerate(lines[839:], start=840):
    print(f"{i:4d}: {repr(line)}")
