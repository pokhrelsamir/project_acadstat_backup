with open(r'core\templates\core\dashboard\upload_marks_excel.html', encoding='utf-8') as f:
    text = f.read()
js_tag = '<script>\n        // Wait for DOM to be ready'
start = text.find(js_tag)
end = text.find('</script>', start)
js = text[start:end]

# Show the FIRST 150 chars of js (which includes <script> wrapper)
print("FIRST 150 chars of js body:")
for i, c in enumerate(js[:150]):
    print(f"  {i:3d}: [{c!r}]")
print()
# Show lines 0-10
lines = js.split('\n')
for i, line in enumerate(lines[:15]):
    print(f"{i+1:3d}: {repr(line[:80])}")
