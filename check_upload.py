import sys
with open('core/templates/core/dashboard/upload_marks_excel.html', encoding='utf-8') as f:
    text = f.read()

start = text.find('<div class="form-actions">')
print(text[start:start+400])
print("---")
# Check for <a> tags near form-actions
idx = text.find('id="uploadArea"')
print("uploadArea context:")
print(text[idx:idx+300])
print("---")
# Check for any outer anchor
for tag in ['<a ', '<a>']:
    pos = text.find(tag)
    if pos >= 0:
        snippet = text[max(0, pos-50):pos+100]
        print(f"Found '{tag}' at {pos}:")
        print(repr(snippet))
