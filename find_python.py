with open(r'core\templates\core\dashboard\upload_marks_excel.html', encoding='utf-8') as f:
    text = f.read()

js_tag = '<script>\n        // Wait for DOM to be ready'
start = text.find(js_tag)
end = text.find('</script>', start)
js = text[start:end]
lines = js.split('\n')

# Find all lines that look like Python (starting with whitespace + identifier)
print("Lines that look like Python-style code (decorators, imports, etc.):")
for i, line in enumerate(lines, 1):
    stripped = line.strip()
    if not stripped: continue
    # Python-style: @decorator, import, from..import, class X:, def X():
    if stripped.startswith('@') or stripped.startswith('import ') or stripped.startswith('from ') or \
       stripped.endswith(':') and not ('function' in stripped or '=>' in stripped or 'if(' in stripped or 'else(' in stripped or 'png' in stripped):
        print(f"  Line {i}: {repr(line.strip()[:80])}")
