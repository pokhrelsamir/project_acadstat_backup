import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'core\templates\core\dashboard\upload_marks_excel.html', encoding='utf-8') as f:
    text = f.read()

# Find and extract just the JS code
start = text.find('<script>\n        // Wait for DOM to be ready')
end_text = '</script>\n      </body>'
end = text.find(end_text, start)
if end <= 0:
    end = text.find('</script>', start)

js = text[start:end]

with open('js_extracted.js', 'w', encoding='utf-8') as out:
    out.write(js)

print("Wrote to js_extracted.js, length:", len(js))
print("First 200 chars:", js[:200])
