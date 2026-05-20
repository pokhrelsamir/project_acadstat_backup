# Check if parenthesis balance after fix is really an issue
# by just doing the balance trace on the HTML file AFTER the fix

with open(r'core\templates\core\dashboard\upload_marks_excel.html', encoding='utf-8') as f:
    text = f.read()

script_start = '<script>\n        // Wait for DOM to be ready'
log = []
brace_bp = paren_bp = 0
i = text.find(script_start)
end = text.find('</script>', i)
print(f"Find script char boundaries: start={i}, end={end}")

# Scan the entire script - just show if paren changes more than brace
js_body = text[i:end]

for idx, c in enumerate(js_body):
    if c == '{': brace_bp += 1
    elif c == '}': brace_bp -= 1
    elif c == '(': paren_bp += 1
    elif c == ')': paren_bp -= 1
    
    # Show last change when both match
    # But show ENTIRE path for parens specifically

print(f"=== FINAL BALANCE ===")
print(f"brace={brace_bp}, paren={paren_bp}")

# If brace=0 and paren=+1, print last 3 chars around the break
print(f"\nScript body last 10 chars: {repr(js_body[-10:])}")

# Verify by doing a MANUAL count of the closing section
closing_section = js_body[js_body.rfind('updateThemeIcon'):]
print(f"\nManual closing section: {repr(closing_section[:200])}...{repr(closing_section[-60:])}")
