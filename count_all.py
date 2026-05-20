"""
Simple approach: show every opening/closing event for braces/parens in the JS body.
Then verify if at the very end the total counts are 0.
"""
with open(r'core\templates\core\dashboard\upload_marks_excel.html', encoding='utf-8') as f:
    text = f.read()

script_start = '<script>\n        // Wait for DOM to be ready'
script_start_pos = text.find(script_start)
end_pos = text.find('</script>', script_start_pos)
js_body = text[script_start_pos:end_pos]

# Check what's right before DOMContentLoaded in the script
dom_pos = js_body.find("DOMContentLoaded")
print(f"DOMContentLoaded starts at js_body pos: {dom_pos}")
ctx = js_body[dom_pos:dom_pos+80]
print(f"  Context: {repr(ctx)}")

# CountALL braces including in JS strings (to confirm whether string braces are included)
total_brace_open = js_body.count('{')
total_brace_close = js_body.count('}')
total_paren_open = js_body.count('(')
total_paren_close = js_body.count(')')
print(f"\nTotal raw counts (no string exclusion):")
print(f"  Brace open {total_brace_open}, close {total_brace_close}, diff {total_brace_open - total_brace_close}")
print(f"  Paren open {total_paren_open}, close {total_paren_close}, diff {total_paren_open - total_paren_close}")
