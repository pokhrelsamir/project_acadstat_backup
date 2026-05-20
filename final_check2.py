with open(r'core\templates\core\dashboard\upload_marks_excel.html', encoding='utf-8') as f:
    text = f.read()

js_start = '<script>\n        // Wait for DOM to be ready'
js_end_marker = '</script>'
start_p = text.find(js_start)
end_p = text.find(js_end_marker, start_p)
js_body = text[start_p:end_p]

print(f"Total chars before </script> tag: {len(js_body)}")

# Balance from start to end (raw character count, NO parsing)
open_braces = js_body.count('{')
close_braces = js_body.count('}')
open_parens = js_body.count('(')
close_parens = js_body.count(')')
print(f"\nRaw character count:")
print(f"  {{ count: {open_braces} open, {close_braces} close")
print(f"  ( count: {open_parens} open, {close_parens} close")

# Map opening brace at position 0 of js_body"
# Position 0 of js_body is the '<' of '<script>', it's the HTML '<', character, it won't be rated.
# But in strict sense, if there is an unmatched '{' in the JavaScript, it must be in the JS code itself.
print(f"\nContent at very start of js_body: {repr(js_body[:20])}")

# Find if there is '{' before the first real JS code
# Position 8 of js_body = '\n' after '<script>'
# Position 9 onwards = '        // Wait for DOM to be ready\n        document.addEventListener('DOMContentLoaded', function() {\n'

# Show the first '{' in the JS body
first_open_brace = js_body.find('{')
first_close_brace = js_body.find('}')
last_open_brace = js_body.rfind('{')
last_close_brace = js_body.rfind('}')
print(f"\nFirst open brace '{{': position {first_open_brace}")
print(f"Context: {repr(js_body[max(0,first_open_brace-10):first_open_brace+10])}")
print(f"First close brace '}}': position {first_close_brace}")
print(f"Context: {repr(js_body[max(0,first_close_brace-10):first_close_brace+10])}")
print(f"Last open brace: position {last_open_brace}")
print(f"Context: {repr(js_body[max(0,last_open_brace-10):last_open_brace+10])}")
print(f"Last close brace: position {last_close_brace}")
print(f"Context: {repr(js_body[max(0,last_close_brace-10):last_close_brace+10])}")
