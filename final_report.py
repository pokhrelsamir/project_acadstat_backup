with open(r'core\templates\core\dashboard\upload_marks_excel.html', encoding='utf-8') as f:
    text = f.read()

# Apply the final definitive fix
# Currently the last part of the JS body is:
#                });   <- catch handler
#            });      <- submit handler
#        });          <- DOMContentLoaded handler (wait, is it actually there?)

js_tag = '<script>\n        // Wait for DOM to be ready'
start = text.find(js_tag)
end = text.find('</script>', start)
js_body = text[start:end]

# Count function() {  openings matched by }); closures
import re

# Find addEventListener with function()
ae_func = [(m.start(), m.group()) for m in re.finditer(r'addEventListener\([^)]*?function\s*\(', js_body)]
print("addEventListener + function() handlers: %d" % len(ae_func))
for pos, match in ae_func:
    print("  pos=%d: %s" % (pos, repr(match[:60])))

# Find all closing });  patterns
closures = [(m.start(), '});') for m in re.finditer(r'\}\);\s*', js_body)]
print("\nAll }); closures: %d" % len(closures))
for pos, pat in closures:
    ctx = js_body[pos-10:pos+10]
    print("  pos=%d: %s" % (pos, repr(ctx)))
    
# Expected: should be NUM_EVENT_BINDINGS closings for addEventListener with function
# PLUS extras for forEach, showToast internals, etc.
# If the DOMContentLoaded handler is matched, the last }); should be the DOMContentLoaded close

# Find DOMContentLoaded handler opening
dcl_pos = js_body.find("DOMContentLoaded", start=0)
print("\nDOMContentLoaded first occurrence at: %d" % dcl_pos)
print("Context: %s" % repr(js_body[dcl_pos:dcl_pos+60]))

# More precise: find the addEventListener for DOMContentLoaded
for pos, match in ae_func:
    if 'DOMContentLoaded' in match or 'DOMContentLoaded' in js_body[pos-20:pos+20]:
        print("  ^ This is the DOMContentLoaded addEventListener at position %d" % pos)
        break

print("\n=== Report ===")
print("DOMContentLoaded addEventListener handler at one of the ae_func positions.")
print("The script ends at position %d (before </script>)." % (len(js_body)))
print("Current last characters: %s" % repr(js_body[-80:]))
should_be = " });\n    "
has_it = js_body[-len(should_be):] == should_be
print("Ends with '});\n    ' as expected: %s" % has_it)
