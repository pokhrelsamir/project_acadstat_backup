with open(r'core\templates\core\dashboard\upload_marks_excel.html', encoding='utf-8') as f:
    lines = f.readlines()
with open('js_extracted.js', encoding='utf-8') as f:
    js_lines = f.readlines()

total_html_js_lines = len(lines[814:864])  # lines 815-864 = 50 lines
print(f"HTML JS section has {len(lines)} total lines")
print(f"Lines 815-865 count: {len(lines[814:865])}")
print(f"js_extracted.js has {len(js_lines)} lines")
print(f"js_extracted.js last line: {repr(js_lines[-1][:100])}")
print()
print("js_extracted.js last 5 lines:")
for i, l in enumerate(js_lines[-5:], len(js_lines)-4):
    print(f"  {i}: {repr(l.rstrip())}")
