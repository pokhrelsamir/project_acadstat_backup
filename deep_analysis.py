"""Deep analysis of the HTML structure to find the div mismatch."""
with open(r'core/templates/core/dashboard/upload_marks_excel.html', encoding='utf-8') as f:
    lines = f.readlines()

# Show lines 460-676 with EXACT indent level and div open/close
# The key question: where does the closing </form> happen and is
# it closing the right div?

out = "Line | Indent | Tag | Content\n"
out += "-" * 80 + "\n"
for i, line in enumerate(lines[459:676], start=460):
    stripped = line.strip()
    leading = len(line) - len(line.lstrip())
    if stripped:
        tag_marker = ""
        if stripped.startswith('<form'):
            tag_marker = "FORM OPEN"
        elif stripped.startswith('</form>'):
            tag_marker = "FORM CLOSE"
        elif stripped.startswith('<div'):
            tag_marker = "DIV OPEN"
        elif stripped == '</div>':
            tag_marker = "DIV CLOSE"
        if tag_marker:
            out += "%4d | %4d | %s | %s\n" % (i, leading, tag_marker, stripped[:80])

out += "\n\n"
out += "ANALYSIS: check if instruction-section at line 591 matches any </div>\n"
out += "Expecting: line 591 (indent 17) is INSIDE the form-card\n"
out += "If be inside form-card, it should be part of <form> and <form-card> structures\n"

print(out)

with open('deep_structure.txt', 'w', encoding='utf-8') as fout:
    fout.write(out)
print("Wrote to deep_structure.txt")
