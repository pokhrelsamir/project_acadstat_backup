with open(r'core\templates\core\dashboard\upload_marks_excel.html', encoding='utf-8') as f:
    lines = f.readlines()

# Show the LAST 5 lines (proving the fix)
print("VERIFICATION: Lines 860-865 NOW show:")
for i, line in enumerate(lines[859:865], start=860):
    print(f"{i:4d}: {repr(line)}")
