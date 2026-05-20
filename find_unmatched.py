with open(r'core\templates\core\dashboard\upload_marks_excel.html', encoding='utf-8') as f:
    text = f.read()
script_start = '<script>\n        // Wait for DOM to be ready'
script_start_pos = text.find(script_start)
end_pos = text.find('</script>', script_start_pos)
js = text[script_start_pos:end_pos]

# Properly count brace differences - just show where
total_open = js.count('{')
total_close = js.count('}')
print(f"JS body {len(js)} chars:")
print(f"  open count: {total_open}")
print(f"  close count: {total_close}")
print(f"  diff: {total_open - total_close}")

brace_count = 0
lines = js.split('\n')
for i, line in enumerate(lines):
    old_count = brace_count
    for c in line:
        if c == '{': brace_count += 1
        elif c == '}': brace_count -= 1
    if brace_count != 0 and brace_count != old_count:
        print(f"  JS line {i+1}: brace {old_count:+d} -> {brace_count:+d}")
