with open(r'core\templates\core\dashboard\upload_marks_excel.html', encoding='utf-8') as f:
    lines = f.readlines()

# Show lines 855-865 to see current state
for i, line in enumerate(lines[854:865], start=855):
    print(f"{i:4d}: {repr(line)}")
print("Total lines:", len(lines))
