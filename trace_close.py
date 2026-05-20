with open(r'core\templates\core\dashboard\upload_marks_excel.html', encoding='utf-8') as f:
    lines = f.readlines()

def scan_until_closebrace(after_line):
    """Starting from after_line (0-indexed), find where the DOMContentLoaded handler closes"""
    brace_p = paren_p = 0
    for i in range(after_line, len(lines)):
        line = lines[i]
        for c in line:
            if c == '{': brace_p += 1
            elif c == '}': brace_p -= 1
            elif c == '(': paren_p += 1
            elif c == ')': paren_p -= 1
        if brace_p <= 0 and paren_p <= 0 and i > after_line:
            print(f"Close reached at line {i+1}: balance brace={brace_p}, paren={paren_p}")
            print(f"  Context: {repr(lines[i][:80])}")
            if i > after_line + 5:
                print(f"  Previous few lines:")
                for j in range(i-5, i+1):
                    print(f"    {j+1}: {repr(lines[j][:100])}")
            break

# Find addEventListener('submit'... line
for i, line in enumerate(lines):
    if 'addEventListener' in line and 'submit' in line and i > 700:
        print(f"submit addEventListener at line {i+1}")
        print(f"  Context: {repr(lines[i][:100])}")
        brace_p = paren_p = 1
        # chars in this line:
        for c in line:
            if c == '{': brace_p += 1
            elif c == '}': brace_p -= 1
            elif c == '(': paren_p += 1
            elif c == ')': paren_p -= 1
        print(f"  After this line: brace={brace_p}, paren={paren_p}")
        scan_until_closebrace(i)
        break
