with open(r'core\templates\core\dashboard\upload_marks_excel.html', encoding='utf-8') as f:
    lines = f.readlines()

# The script starts at line 681 (0-indexed 680)
# and ends at the </script>
def find_balance_at_line(text, target_line_1idx):
    brace_bp = paren_bp = 0
    all_lines = text.split('\n')
    for i, line in enumerate(all_lines):
        # Only count lines before target including it
        if i + 1 <= target_line_1idx:
            for c in line:
                if c == '{': brace_bp += 1
                elif c == '}': brace_bp -= 1
                elif c == '(': paren_bp += 1
                elif c == ')': paren_bp -= 1
    return brace_bp, paren_bp

text = ''.join(lines)
script_start_pos = text.find('<script>\n        // Wait for DOM to be ready')
print(f"Script start position: {script_start_pos}")

# We need to IDENTIFY line numbers FROM THE ACTUAL FILE
script_start_line = text[:script_start_pos].count('\n') + 1  # 1-indexed
print(f"Script starts at HTML line number: {script_start_line}")

# Now scan braces from script start
script_text = text[script_start_pos:]
brace_bp = paren_bp = 0
results = []
lines_script = script_text.split('\n')
for i, line in enumerate(lines_script[:200]):  # first 200 lines of script
    old_brace = brace_bp
    old_paren = paren_bp
    for c in line:
        if c == '{': brace_bp += 1
        elif c == '}': brace_bp -= 1
        elif c == '(': paren_bp += 1
        elif c == ')': paren_bp -= 1
    if brace_bp > 3:
        results.append((i+1, old_brace, brace_bp, old_paren, paren_bp, line.strip()))
        if len(results) >= 30:
            break

print("All brace changes with balance > 3:")
for r in results:
    print(f"Line {r[0]:4d}: brace {r[1]:+d}->{r[2]:+d}, paren {r[3]:+d}->{r[4]:+d} | {r[5][:80]}")

print()
print("=== FULL BRACE/PAREN TRACE OF LAST 30 LINES OF SCRIPT ===")
script_end_line = script_text.find('</script>')  # position in script
print(f"Script end '</script>' at script-relative char {script_end_line}")
# Do full scan
brace_bp = paren_bp = 0
all_changes = []
for i, line in enumerate(lines_script):
    old_brace = brace_bp; old_paren = paren_bp
    for c in line: 
        if c == '{': brace_bp += 1
        elif c == '}': brace_bp -= 1
        elif c == '(': paren_bp += 1
        elif c == ')': paren_bp -= 1
    if brace_bp != old_brace or paren_bp != old_paren:
        all_changes.append((i+1, old_brace, brace_bp, old_paren, paren_bp))
        
print(f"All brace/paren changes ({len(all_changes)}):")
for r in all_changes[-40:]:
    lineno = script_start_line + r[0] - 1
    print(f"HTML line {lineno:4d} (script {r[0]:3d}): brace {r[1]:+d}->{r[2]:+d}, paren {r[3]:+d}->{r[4]:+d}")
print(f"\nFINAL: brace={brace_bp}, paren={paren_bp}")
