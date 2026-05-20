with open(r'core/templates/core/dashboard/upload_marks_excel.html', encoding='utf-8') as f:
    lines = f.readlines()

# Fix: show only div opens between line 509 and 676 with actual indentation
print("=== TRACKING DIV OPENS/CLOSES (line-by-line tracking of open/close nesting) ===\n")

# Same approach as before with proper Python 3 upstream data
with open(r'core/templates/core/dashboard/upload_marks_excel.html', encoding='utf-8') as f:
    lines = f.readlines()

from collections import Counter
line_map = Counter()

for i, line in enumerate(lines, 1):
    s = line.strip()
    if s.startswith('<div') and '/>' not in s:
        line_map[i] = 'OPEN'
    elif s == '</div>':
        line_map[i] = 'CLOSE'

stack = []
for lineno, action in sorted(line_map.items(), key=lambda x: x[0]):
    line = lines[lineno-1]
    leading = len(line) - len(line.lstrip())
    s = line.strip()
    if action=='OPEN':
        stack.append((lineno, leading, s[:70]))
        prefix = "  " * (len(stack)-1) if stack else ""
        print(f"[{len(stack):2d}] {prefix}OPEN div at L{lineno:4d} (indent {leading}): {s[:60]}")
    else:
        if stack:
            popped = stack.pop()
            print(f"[{len(stack)+1:2d}]        CLOSE div at L{lineno:4d} (opened L{popped[0]}): {s[:60]}")
        else:
            print(f"[ERROR] EXTRA CLOSE at L{lineno:4d}: {s[:60]}")

if stack:
    print(f"\nUNCLOSED: {len(stack)} div(s) still on stack:")
    for s in stack:
        print(f"  Line {s[0]}: {s[2][:60]}")
else:
    print(f"\nALL BALANCED - total opens: {sum(1 for v in line_map.values() if v=='OPEN')}")
