with open(r'core\templates\core\dashboard\upload_marks_excel.html', encoding='utf-8') as f:
    text = f.read()
js_tag = '<script>\n        // Wait for DOM to be ready'
start = text.find(js_tag)
end = text.find('</script>', start)
js = text[start:end]

import re
open_count = js.count('{')
close_count = js.count('}')
print("Brace summary: open=%d, close=%d, diff=%d" % (open_count, close_count, open_count - close_count))

func_opens = [m.start() for m in re.finditer(r'function\(', js)]
closing = [m.start() for m in re.finditer(r'\);\s*', js)]

print("\nfunction( at positions:")
for pos in func_opens:
    print("  pos=%d: %s" % (pos, repr(js[pos-10:pos+15])))

print("\nClosing patterns (});) at positions:")
for pos in closing:
    ctx = js[pos-20:pos+10]
    print("  pos=%d: %s" % (pos, repr(ctx)))

# Show 3 char BEFORE each close at the end
if closing:
    last_pos = closing[-1]
    print("\nLAST close pos=%d:" % last_pos)
    print("  Context: %s" % repr(js[last_pos-20:last_pos+20]))
