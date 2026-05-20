"""
Verify complete JS balance for upload_marks_excel.html.
"""
with open(r'core\templates\core\dashboard\upload_marks_excel.html', encoding='utf-8') as f:
    text = f.read()

js_tag = '<script>\n        // Wait for DOM to be ready'
start = text.find(js_tag)
end = text.find('</script>', start)
js_body = text[start:end]

print(f"Script length: {len(js_body)}")
print(f"Braces: {js_body.count('{')} open, {js_body.count('}')} close")
print(f"Parens: {js_body.count('(')} open, {js_body.count(')')} close")
print()

# Find closing brace after the last backtick closing
# The three }; sequences
last_backtick = js_body.rfind('`')
print(f"Last backtick at position: {last_backtick}")
print(f"After backtick: {repr(js_body[last_backtick:last_backtick+20])}")

# Find closing DOMContentLoaded } sequence
# DOMContentLoaded, function() { opens at position ~92 (after DOM... line)
dcl_pos = js_body.find("DOMContentLoaded")
print(f"\nDOMContentLoaded at: {dcl_pos}")
dcl_ctx = js_body[dcl_pos:dcl_pos+60]
print(f"  Context: {repr(dcl_ctx)}")

# Find function open after DOMContentLoaded 
func_open = js_body.find('function() {', dcl_pos)
print(f"\nfunction() {{ after DOMContentLoaded: {func_open}")
print(f"  Context: {repr(js_body[func_open:func_open+30])}")

# All }); patterns after the last < backtick
last_close = js_body[last_backtick:]
# Find all }; patterns
pos = 0
while True:
    idx = last_close.find('});', pos)
    if idx < 0:
        break
    actual_pos = last_backtick + idx
    print(f"  Found '}})' at position {actual_pos} (content: {repr(js_body[actual_pos-5:actual_pos+5])})")
    pos = idx + 1
    
# Count all }); patterns in full script
print(f"\nAll '}})' occurrences in JS body:")
all_pos = 0
count = 0
while True:
    idx = js_body.find('});', all_pos)
    if idx < 0: break
    print(f"  At {idx}: {repr(js_body[idx-10:idx+5])}")
    all_pos = idx + 1
    count += 1
print(f"\nTotal '}})' occurrences: {count}")
