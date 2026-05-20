with open(r'core\templates\core\dashboard\upload_marks_excel.html', encoding='utf-8') as f:
    lines = f.readlines()
with open('lines_800_865.txt', 'w', encoding='utf-8') as out:
    for i, line in enumerate(lines[799:865], start=800):
        out.write(f"{i:4d}: {repr(line)}\n")
print("Written lines_800_865.txt")
