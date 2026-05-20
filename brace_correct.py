with open(r'core\templates\core\dashboard\upload_marks_excel.html', encoding='utf-8') as f:
    text = f.read()

def get_brace_balance(js_body):
    """
    Count braces/parens in js_body, correctly handling:
    - template literals (backtick strings)
    - regular strings (single/double quoted)
    - comments (// and /* */)
    """
    brace = paren = 0
    i = 0
    length = len(js_body)
    
    while i < length:
        c = js_body[i]
        
        # Template literal: backtick
        if c == '`':
            i += 1
            while i < length and js_body[i] != '`':
                if js_body[i] == '\\':  # escape in template literals
                    i += 2
                    continue
                i += 1
            continue
        
        # Double-quoted string
        if c == '"':
            i += 1
            while i < length and js_body[i] != '"':
                if js_body[i] == '\\': i += 2; continue
                i += 1
            continue
        
        # Single-quoted string
        if c == "'":
            i += 1
            while i < length and js_body[i] != "'":
                if js_body[i] == '\\': i += 2; continue
                i += 1
            continue
        
        if c == '/' and i + 1 < length:
            if js_body[i+1] == '/':  # line comment
                while i < length and js_body[i] != '\n':
                    i += 1
                continue
            if js_body[i+1] == '*':  # block comment
                i += 2
                while i < length - 1 and not (js_body[i] == '*' and js_body[i+1] == '/'):
                    i += 1
                if i < length - 1:
                    i += 2
                continue
        
        if c == '{': brace += 1
        elif c == '}': brace -= 1
        elif c == '(': paren += 1
        elif c == ')': paren -= 1
        
        i += 1
    
    return brace, paren

# Get the JS body (between <script> and </script>)
start_tag = '<script>\n        // Wait for DOM to be ready'
script_start = text.find(start_tag)
end_tag = text.find('</script>', script_start)
js_body = text[script_start:end_tag]
print(f"Script length: {len(js_body)}")
print(f"Script ends with: {repr(js_body[-50:])}")

brace, paren = get_brace_balance(js_body)
print(f"\nBrace balance: {brace}")
print(f"Paren balance: {paren}")

# Also check by line to find exactly where imbalance is at the end
brace_p2 = paren_p2 = 0
results = []
js_lines = js_body.split('\n')
for i, line in enumerate(js_lines):
    old_b = brace_p2; old_p = paren_p2
    # Use simple character counting per line (without string awareness)
    # Manually parse inline
    j = 0
    line_content = line
    while j < len(line_content):
        c = line_content[j]
        if c == '`':
            j += 1
            while j < len(line_content) and line_content[j] != '`':
                if line_content[j] == '\\': j += 2; continue
                j += 1
            continue
        if c == '"':
            j += 1
            while j < len(line_content) and line_content[j] != '"':
                if line_content[j] == '\\': j += 2; continue
                j += 1
            continue
        if c == "'":
            j += 1
            while j < len(line_content) and line_content[j] != "'":
                if line_content[j] == '\\': j += 2; continue
                j += 1
            continue
        if c == '{': brace_p2 += 1
        elif c == '}': brace_p2 -= 1
        elif c == '(': paren_p2 += 1
        elif c == ')': paren_p2 -= 1
        j += 1
    if brace_p2 != old_b or paren_p2 != old_p:
        results.append((i+1, old_b, brace_p2, old_p, paren_p2, line.strip()))

print(f"\nBalance changes with template literal awareness ({len(results)} total):")
for r in results[-30:]:
    print(f"  JS Line {r[0]:4d}: brace {r[1]:+d}->{r[2]:+d}, paren {r[3]:+d}->{r[4]:+d} | {r[5][:80]}")
print(f"\nFinal: brace={brace_p2}, paren={paren_p2}")
