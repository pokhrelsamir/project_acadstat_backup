with open(r'core\templates\core\dashboard\upload_marks_excel.html', encoding='utf-8') as f:
    text = f.read()
script_start = 28121
script_end = 37362
actual_script = text[script_start:script_end]

brace_balance = 0
paren_balance = 0
lines = actual_script.split('\n')
results = []

for i, line in enumerate(lines):
    old_brace = brace_balance
    old_paren = paren_balance
    for c in line:
        if c == '{': brace_balance += 1
        elif c == '}': brace_balance -= 1
        elif c == '(': paren_balance += 1
        elif c == ')': paren_balance -= 1
    if brace_balance != old_brace or paren_balance != old_paren:
        results.append((i+1, old_brace, brace_balance, old_paren, paren_balance, line.strip()))

print(f"Total lines: {len(lines)}")
print(f"Final brace balance: {brace_balance}")
print(f"Final paren balance: {paren_balance}")
print()
print("Lines where braces/parens changed:")
for line_no, ob, nb, op, np, l in results[-50:]:
    print(f"Line {line_no:4d}: brace {ob:+d}->{nb:+d}, paren {op:+d}->{np:+d} | {l[:80]}")
    