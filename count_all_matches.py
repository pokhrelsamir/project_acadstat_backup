with open(r'core\templates\core\dashboard\upload_marks_excel.html', encoding='utf-8') as f:
    text = f.read()
js_tag = '<script>\n        // Wait for DOM to be ready'
start = text.find(js_tag)
end = text.find('</script>', start)
js = text[start:end]

import re
func_patterns = []
for m in re.finditer(r'addEventListener\([^)]*function\s*\(', js):
    p = m.start()
    ctx = js[p:p+80]
    func_patterns.append(p)
    
print("event-bindings found: %d" % len(func_patterns))
for p in func_patterns:
    ctx = js[p:p+60]
    print("  pos=%d: %s" % (p, repr(ctx)))

open_b = js.count('{')
close_b = js.count('}')
open_p = js.count('(')
close_p = js.count(')')
print("\nBrace: open=%d close=%d diff=%d" % (open_b, close_b, open_b-close_b))
print("Paren: open=%d close=%d diff=%d" % (open_p, close_p, open_p-close_p))

closes = []
search = 0
while True:
    m = re.search(r'\}\);\s*', js[search:])
    if not m: break
    pos = search + m.start()
    ctx = js[pos-15:pos+15]
    closes.append((pos, ctx))
    search = pos + 1
print("\nTotal close }); patterns: %d" % len(closes))
print("Last positions:")
for target in [8450, 6600, 9200]:
    idx = None
    for i, (pos, ctx) in enumerate(closes):
        if abs(pos - target) <= 2:
            idx = i
            break
    if idx is not None:
        print("  Near %d: %s" % (target, closes[idx]))
