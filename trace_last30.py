with open(r'core\templates\core\dashboard\upload_marks_excel.html', encoding='utf-8') as f:
    text = f.read()
js_tag = '<script>\n        // Wait for DOM to be ready'
start = text.find(js_tag)
end = text.find('</script>', start)
js = text[start:end]
lines = js.split('\n')

post_text = []
# Display last 40 lines of script body
print("Showing last 40 JS body lines (<script> portion only):")
for i, line in enumerate(lines[-40:], start=len(lines)-39):
    stripped = line.strip()
    print(f"  {i:4d}: {repr(stripped[:80])}")

last30 = '\n'.join(lines[-30:])
open_b = last30.count('{')
close_b = last30.count('}')
open_p = last30.count('(')
close_p = last30.count(')')

print(f"\nLast 30 lines stats:")
print(f"  '(' count: {open_p}, ')' count: {close_p}")
print(f"  'open brace' count: {open_b}, 'close brace' count: {close_b}")
