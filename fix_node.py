with open(r'core\templates\core\dashboard\upload_marks_excel.html', encoding='utf-8') as f:
    text = f.read()
# Inline script starts with '        // Wait for DOM to be ready'
# but actually start at after <script>\n
script_start = text.find('<script>\n') + len('<script>\n')
script_end = text.find('</script>', script_start)
with open('js_for_node.js', 'w', encoding='utf-8') as out:
    out.write(text[script_start:script_end])
print(f"Wrote {script_end - script_start} chars to js_for_node.js")
