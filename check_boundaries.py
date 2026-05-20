with open(r'core\templates\core\dashboard\upload_marks_excel.html', encoding='utf-8') as f:
    text = f.read()
js_start = '<script>\n        // Wait for DOM to be ready'
start_p = text.find(js_start)
end_p = text.find('</script>', start_p)
js = text[start_p:end_p]
# Get the first 100 chars of js and last 100 chars
print("First 100 chars of JS body:")
for i, c in enumerate(js[:100]):
    print(f"  {i}: [{c!r}]")
print("\nLast 100 chars of JS body:")
for i, c in enumerate(js[-100:], len(js)-99):
    print(f"  {i}: [{c!r}]")
