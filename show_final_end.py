with open(r'core\templates\core\dashboard\upload_marks_excel.html', encoding='utf-8') as f:
    lines = f.readlines()
with open('final_end_lines.txt', 'w', encoding='utf-8') as out:
    for i, line in enumerate(lines[801:865], start=802):
        out.write(f"{i:4d}: {repr(line)}\n")
print("Written to final_end_lines.txt")
