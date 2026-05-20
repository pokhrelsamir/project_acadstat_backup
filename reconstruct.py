"""Reconstruct the actual content from key character positions."""
with open(r'core/templates/core/dashboard/upload_marks_excel.html', encoding='utf-8') as f:
    text = f.read()

# Show well over 300 lines to see EVERYTHING from form-group1 through form-card close
start_pos = text.find('<form method="POST"')
end_pos = text.find('</script>')

sub = text[start_pos:end_pos]

with open('full_section.txt', 'w', encoding='utf-8') as out:
    out.write(sub)
print("Wrote section to full_section.txt (%d chars)" % len(sub))
print(f"Section length: {len(sub)} chars")
