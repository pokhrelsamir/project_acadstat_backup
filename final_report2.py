with open(r'core\templates\core\dashboard\upload_marks_excel.html', encoding='utf-8') as f:
    text = f.read()
js_tag = '<script>\n        // Wait for DOM to be ready'
start = text.find(js_tag)
end = text.find('</script>', start)
js_body = text[start:end]

import re
ae_func_positions = [(m.start(), m.group()[:60]) for m in re.finditer(r'addEventListener\([^)]*?function\s*\(', js_body)]
closures = [(m.start()) for m in re.finditer(r'\}\);\s*', js_body)]

print("addEventListener with function() handlers: %d" % len(ae_func_positions))
for pos, match in ae_func_positions:
    ctx = js_body[pos:pos+70]
    print("  pos=%d: %s" % (pos, repr(ctx)))

print("\n}); closes: %d" % len(closures))
print("Last 5 closes: %s" % closures[-5:])
print("\nExpected: {event_handlers} + {forEach/showToast filters} + {async/etc}")

# Now verify
ae_positions = [p for p, _ in ae_func_positions]
if len(closures) >= len(ae_positions):
    # Get the last N closings corresponding to the last N ae openers
    # Check if the last DOMContentHandler closing matches PATTERN
    print("\nMapping handlers to their position changes:")
    closures_last = closures[-len(ae_positions):]  # last N closures
    for i, (ae_pos, close_pos) in enumerate(zip(ae_positions, closures_last)):
        ctx = js_body[ae_pos:ae_pos+50]
        print("  [%d] AE at %5d: %s -> close at %5d (diff %5d)" % (
            i, ae_pos, repr(ctx[:40].split(',')[0]+')'), close_pos, close_pos-ae_pos))
else:
    print("More closures than addEventBindings!")

# Direct verification
# The last ADDEventListener handler (submit, pos=6584) should be the last N-n handler
print("\nTelepot check:")
for i, (ae_pos, close_pos) in enumerate(zip(ae_positions, closures[-len(ae_positions):])):
    ctx = js_body[ae_pos:ae_pos+60]
    print("  Match $ ae=%s close=%s (diff=%d)" % (repr(ctx[:40]), '', close_pos-ae_pos))

open_b = js_body.count('{')
close_b = js_body.count('}')
print("\nBrace at body-level: open=%d close=%d diff=%d" % (open_b, close_b, open_b-close_b))

# Show last 120 chars to confirm correct closing
print("\nLast 120 chars:")
print(repr(js_body[-120:]))
