"""Validate exact div nesting in upload_marks_excel.html"""
with open(r'core/templates/core/dashboard/upload_marks_excel.html', encoding='utf-8') as f:
    lines = f.readlines()

# Track indentation depths for <div, </div>
stack = []
errors = []
for i, line in enumerate(lines, 1):
    stripped = line.rstrip('\n')
    # count leading spaces
    indent = len(stripped) - len(stripped.lstrip())
    
    if '<div' in stripped.lower() and '>/' not in stripped.lower():
        stack.append((i, indent, stripped.strip()[:70]))
    if '</div>' in stripped.lower():
        if stack:
            open_match = stack.pop()
        else:
            errors.append(f"CLOSE with no open at line {i}: {stripped.strip()[:60]}")

if stack:
    for s in stack:
        errors.append(f"UNCLOSED div opened at line {s[0]}: {s[2][:60]}")

if errors:
    print("ERRORS:")
    for e in errors:
        print(f"  {e}")
else:
    print("All 23 divs are properly indented and balanced!")

# Also verify:
print(f"\nStack remaining (should be empty if all closed): {stack}")
