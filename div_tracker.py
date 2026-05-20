"""Find all unaccounted-for div opens by tracking nesting properly."""
with open(r'core/templates/core/dashboard/upload_marks_excel.html', encoding='utf-8') as f:
    lines = f.readlines()

# Map indentation to stack depth
# We'll EXPLICITLY track each open/close div
class Node:
    def __init__(self, lineno, indent, tag):
        self.lineno = lineno
        self.indent = indent
        self.tag = tag
        self.open = True

stack = []
rounds = []

for i, line in enumerate(lines, 1):
    stripped = line.strip()
    if not stripped:
        continue
    if stripped.startswith('<div') and '>' in stripped and not '/>' in stripped:
        leading = len(line) - len(line.lstrip())
        stack.append((i, leading, stripped[:60]))
        rounds.append(('OPEN', i, leading, stripped[:60]))
    elif stripped == '</div>':
        if stack:
            popped = stack.pop()
            rounds.append(('CLOSE', i, popped[0], popped[2]))
        else:
            rounds.append(('ORPHAN-CLOSE', i, -1, stripped[:60]))

# After EOF, report remaining open divs
if stack:
    print("REMAINING OPEN DIVS (not closed):")
    for s in stack:
        print(f"  Line {s[0]}: {repr(s[2])}")
else:
    print("All divs balanced.")

# Now show the flow around the instructions-section area
for event_type, lineno, level, content in rounds:
    if lineno >= 460 and lineno <= 680:
        if event_type in ('OPEN', 'CLOSE'):
            print(f"  {event_type:10s} Line {lineno:4d} | {content[:70]}")
