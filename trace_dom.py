with open(r'core\templates\core\dashboard\upload_marks_excel.html', encoding='utf-8') as f:
    lines = f.readlines()

# Find and track DOMContentLoaded
brace_p = paren_p = 0
for i, line in enumerate(lines):
    for c in line:
        if c == '{': brace_p += 1
        elif c == '}': brace_p -= 1
        elif c == '(': paren_p += 1
        elif c == ')': paren_p -= 1
    if 'DOMContentLoaded' in line and 'function' in line:
        # Opening event
        print(f"Opening at line {i+1}: after this line brace={brace_p}, paren={paren_p}")
        print(f"  Line: {repr(line[:100])}")
    if paren_p <= 0 and brace_p == 0 and i >= 680:
        if brace_p == 0:
            print(f"Final close at line {i+1}: brace={brace_p}, paren={paren_p}")
            print(f"  Line: {repr(line[:100])}")
            print(f"  Last 10 lines of context:")
            for j in range(max(0, i-9), i+1):
                print(f"    {j+1}: {repr(lines[j][:100])}")
            break

print(f"\nFinal balance after scan: brace={brace_p}, paren={paren_p}")
