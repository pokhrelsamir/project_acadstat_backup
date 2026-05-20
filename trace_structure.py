"""Check the structure of upload_marks_excel.html for proper nesting."""
with open(r'core/templates/core/dashboard/upload_marks_excel.html', encoding='utf-8') as f:
    lines = f.readlines()

total_divs_open = 0
total_divs_close = 0
total_forms_open = 0
total_forms_close = 0
total_labels_open = 0
total_labels_close = 0

for i, line in enumerate(lines, 1):
    stripped = line.strip()
    # Count <div> but ignore self-closing or inside comments
    lower = line.lower()
    if '<div' in lower and '<div ' in lower:
        total_divs_open += 1
    if '</div>' in lower:
        total_divs_close += 1
    if '<form' in lower:
        total_forms_open += 1
    if '</form>' in lower:
        total_forms_close += 1
    if '<label' in lower:
        total_labels_open += 1
    if '</label>' in lower:
        total_labels_close += 1

print(f"Div:       {total_divs_open} open, {total_divs_close} close")
print(f"Form:      {total_forms_open} open, {total_forms_close} close")
print(f"Label:     {total_labels_open} open, {total_labels_close} close")

difference = total_divs_open - total_divs_close
form_diff = total_forms_open - total_forms_close
print(f"\nDiv mismatch: {difference}")
print(f"Form mismatch: {form_diff}")
if difference == 0 and form_diff == 0:
    print("HTML structure: BALANCED (may still be mis-nested)")
else:
    print("HTML structure: UNBALANCED!")
    if difference > 0:
        print(f"  {difference} extra div(s) opened but not closed")
    elif difference < 0:
        print(f"  {-difference} extra div(s) closed but not opened")
    if form_diff > 0:
        print(f"  {form_diff} extra form(s) opened but not closed")
    elif form_diff < 0:
        print(f"  {-form_diff} extra form(s) closed but not opened")
