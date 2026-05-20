with open(r'core\templates\core\dashboard\upload_marks_excel.html', encoding='utf-8') as f:
    lines = f.readlines()

# And later:
with open(r'core\templates\core\dashboard\upload_marks_excel.html', encoding='utf-8') as f:
    full_text = f.read()

# Parse brace/paren correctly (ignoring strings and regexp)
def js_aware_balance(text_body):
    brace = paren = 0
    i = 0
    length = len(text_body)
    while i < length:
        c = text_body[i]
        # Template literal (backtick)
        if c == '`':
            i += 1
            while i < length and text_body[i] != '`':
                if text_body[i] == '\\': i += 2; continue
                i += 1
            continue
        # Single/double quoted strings
        if c in '\'"':
            quote = c
            i += 1
            while i < length and text_body[i] != quote:
                if text_body[i] == '\\': i += 2; continue
                i += 1
            continue
        # Regexp... - complex, skip for now
        if c == '/':
            if i + 1 < length and text_body[i+1] not in '/*':
                i += 1
                while i < length and text_body[i] not in '/\n':
                    if text_body[i] == '\\': i += 2; continue
                    i += 1
                continue
        
        if c == '{': brace += 1
        elif c == '}': brace -= 1
        elif c == '(': paren += 1
        elif c == ')': paren -= 1
        i += 1
    
    return brace, paren

# Get JS body ONLY (between <script> and </script> tags)
script_before = '<script>\n        // Wait for DOM to be ready'
script_after = '</script>'
script_start = full_text.find(script_before)
script_end = full_text.index(script_after, script_start)
js_body = full_text[script_start:script_end]

print(f"JS body starts: {repr(js_body[:50])}")
print(f"JS body ends:   {repr(js_body[-50:])}")
brace, paren = js_aware_balance(js_body)
print(f"\nJS-aware balance: brace={brace}, paren={paren}")

# Also just count chars in final analyzed section
# Print last few lines' content actually inside HTML
print("\nHTML lines 858-865 from file:")
for i, line in enumerate(lines[857:865], start=858):
    print(f"  {i}: {repr(line)}")
