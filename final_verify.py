"""
Final verification of the upload_marks_excel.html JavaScript.
Count braces/parens, and verify the DOMContentLoaded handler is properly closed.
"""
with open(r'core\templates\core\dashboard\upload_marks_excel.html', encoding='utf-8') as f:
    text = f.read()
lines = text.split('\n')

# Simple check: find the outer DOMContentLoaded handler body
# and verify it closes at the very end of the script
script_start = text.find('<script>\n        // Wait for DOM to be ready')
end_pos = text.find('</script>', script_start)
js_body = text[script_start:end_pos]

brace = paren = 0
changes = []
for i, line in enumerate(js_body.split('\n'), 1):
    old_brace, old_paren = brace, paren
    for c in line:
        if c == '{': brace += 1
        elif c == '}': brace -= 1
        elif c == '(': paren += 1
        elif c == ')': paren -= 1
    if brace != old_brace or paren != old_paren:
        changes.append((i, old_brace, brace, old_paren, paren, line.strip()[:80]))

if changes:
    print("All balance changes:")
    for r in changes:
        print(f"  Line {r[0]:4d}: brace {r[1]:+d}->{r[2]:+d}, paren {r[3]:+d}->{r[4]:+d} | {r[5]}")
else:
    print("No changes found!")

# Show final 10 changes
print("\nLast 15 balance changes:")
for r in changes[-15:]:
    print(f"  Line {r[0]:4d}: brace {r[1]:+d}->{r[2]:+d}, paren {r[3]:+d}->{r[4]:+d}")

result = "PASS" if brace == 0 and paren == 0 else "FAIL"
print(f"\n=== RESULT: {result} ===")
print(f"Brace balance: {brace} {'✓' if brace == 0 else '✗ (expected 0)'}")
print(f"Paren balance: {paren} {'✓' if paren == 0 else '✗ (expected 0)'}")

print(f"\nScript ends with last 60 chars:")
print(f"  {repr(js_body[-60:])}")
print(f"\nJS body length: {len(js_body)}")
print(f"HTML file total char length: {len(text)}")
print(f"Line count total: {len(lines)}")

# Also verify that the exact `});` appears in the HTML file at the right place
needle = '            });\n    </script>\n'
idx = text.find(needle, lines[0:859][-1::-1])  # search backwards from end
print(f"\nChecking for '}})\\n    </script>' in HTML: found at {text.find(needle)}")
print(f"Better: end of script context (last 80 chars before </script>):")
last_80 = js_body[-80:]
print(f"  {repr(last_80)}")
