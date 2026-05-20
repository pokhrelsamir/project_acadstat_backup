"""Analyze the exact nesting of last 20 lines of the HTML template."""
with open(r'core/templates/core/dashboard/upload_marks_excel.html', encoding='utf-8') as f:
    lines = f.readlines()

# Find the FORM and FORM-CARD and INSTRUCTIONS closes
# Show actual leading whitespace (not stripped content) for context
# of lines 509, 515, 565, 568, 589, 591, 673, 674, 675, 676

key_lines = [511, 515, 531, 549, 568, 591, 673, 674, 675, 676, 8858, 8859, 8860, 8861]
for lineno in key_lines:
    if lineno <= len(lines):
        line = lines[lineno-1]
        leading = len(line) - len(line.lstrip())
        print(f"Line {lineno:4d}: [indent={leading}] {repr(line.rstrip()[:100])}")

print("\n--- Also verify open/close balance for div ---")
# With leading whitespace detection
div_open = 0
div_close = 0
for i, line in enumerate(lines, 1):
    # use stripped check but better approach: only count if tag starts a line
    stripped = line.strip()
    if stripped.startswith('<div'):
        # make sure it's not something like s<div 
        if not stripped[-1] == '>' or ('/>' in stripped):
            continue
        # separate check: count actual opening divs at start (not comments etc)
        if stripped.startswith('<div ') or stripped.startswith('<div'):
            div_open += 1
    if stripped == '</div>':
        div_close += 1
        
print(f"Opening divs: {div_open}")
print(f"Closing divs: {div_close}")
print(f"Balance: {div_open - div_close}")
