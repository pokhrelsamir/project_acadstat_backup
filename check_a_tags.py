# Find all HTML attribute "onClick" "onsubmit" in upload template
import sys

with open('core/templates/core/dashboard/upload_marks_excel.html', encoding='utf-8') as f:
    text = f.read()

# Find any hardcoded paths in the HTML (local URLs that aren't Django URL tags)
import re
# Find hardcoded URLs (not Django {% url %} tags)
lines = text.split('\n')
for i, line in enumerate(lines, 1):
    if 'href="/' in line or 'action="' in line:
        print(f'{i:4d}: {line.strip()[:100]}')
print("---")
# Find first 50 occurrences of <a or <form
count = 0
for i, line in enumerate(lines, 1):
    if '<a ' in line or '<form' in line:
        print(f'{i:4d}: {line.strip()[:100]}')
        count += 1
        if count >= 50:
            break
print(f"Total <a> and <form> found: {count}")
print("---")
# Find any form elements
count = 0
for i, line in enumerate(lines, 1):
    if 'name="' in line and 'excel_file' not in line:
        count += 1
