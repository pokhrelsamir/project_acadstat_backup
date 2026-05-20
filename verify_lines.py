with open(r'core\templates\core\dashboard\upload_marks_excel.html', encoding='utf-8') as f:
    text = f.read()
script_start = 28121
script_end_text = '</script>'
end_pos = text.find(script_end_text, script_start)
print("end_pos =", end_pos)
print("Script will run from char", script_start, "to", end_pos, "length:", end_pos - script_start)
actual_script = text[script_start:end_pos]
print("Actual script ends with:", repr(actual_script[-30:]))
lines = actual_script.split('\n')
print("Lines:", len(lines))
print("Line 186 content:", repr(lines[185]))
if len(lines) > 186:
    print("Line 187:", repr(lines[186]))
