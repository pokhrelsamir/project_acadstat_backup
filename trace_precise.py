with open(r'core\templates\core\dashboard\upload_marks_excel.html', encoding='utf-8') as f:
    lines = f.readlines()

def count_script_balance(start_line, end_line):
    brace_bp = paren_bp = 0
    results = []
    for i in range(start_line, end_line):
        line = lines[i]  # 0-indexed
        line_no = i + 1
        old_brace = brace_bp
        old_paren = paren_bp
        for c in line:
            if c == '{': brace_bp += 1
            elif c == '}': brace_bp -= 1
            elif c == '(': paren_bp += 1
            elif c == ')': paren_bp -= 1
        if brace_bp != old_brace or paren_bp != old_paren:
            results.append((line_no, old_brace, brace_bp, old_paren, paren_bp, line.rstrip()))
    return results, brace_bp, paren_bp

# Count from line 815 (JS file line 815) to line 862 (JS file line 862=1-indexed) + line 863
# Using 0-indexed Python indices
results, final_brace, final_paren = count_script_balance(815, 864)

for r in results:
    print(f"Line {r[0]:4d}: brace {r[1]:+d}->{r[2]:+d}, paren {r[3]:+d}->{r[4]:+d} | {r[5][:90]!r}")

print(f"\nFinal brace balance: {final_brace}")
print(f"Final paren balance: {final_paren}")
