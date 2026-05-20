"""Show the exact spaces/tabs at key lines to confirm the actual nesting."""
with open(r'core/templates/core/dashboard/upload_marks_excel.html', encoding='utf-8') as f:
    lines = f.readlines()

print("=== Key lines with actual ASCII characters ===")
key_lines = [465, 511, 568, 591, 592, 673, 674, 675, 676, 8458, 8459, 8460, 8461]
for lineno in key_lines:
    if lineno <= len(lines):
        line = lines[lineno-1]
        # Show actual characters in first 80
        visible = []
        for c in line[:80]:
            if c == ' ': visible.append('·')
            elif c == '\t': visible.append('→')
            else: visible.append(c)
        print(f"L{lineno:4d}: indent={len(line) - len(line.lstrip())} | {''.join(visible)}")
