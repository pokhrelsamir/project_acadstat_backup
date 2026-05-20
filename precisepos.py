with open(r'core\templates\core\dashboard\upload_marks_excel.html', encoding='utf-8') as f:
    text = f.read()

print("Content immediately BEFORE <script> tag at position 28121 char:")
script_pos = text.find('<script>')
for i in range(max(0, script_pos-50), script_pos+20):
    print(f"  {i}: [{text[i]!r}]")

# Find 'function(' occurrences before script start
before_script = text[:script_pos]
print("\nSearching for any function( or similar patterns before <script>...")
import re
for m in re.finditer(r'function\s*\(', before_script):
    pos = m.start()
    print(f"  Found 'function(' at position {pos}: {repr(before_script[pos-30:pos+20])}")
for m in re.finditer(r'\bfunction\b.*\{', before_script):
    pos = m.start()
    print(f"  Found 'function...' at position {pos}: {repr(before_script[pos-30:pos+20])}")

# Narrow scope - just check if there is a FORBIDDEN TAG+BODY that could have '{' mismatched
# This would likely be CSS-style vars() or style="", CSS that uses {} or any hidden syntax 
print("\nChecking for malformed syntax near script boundaries:")
pre_ctx = text[max(0,script_pos-100):script_pos]
post_ctx = text[text.find('</script>', script_pos):text.find('</script>', script_pos)+50]
print(f"Before <script> last 100 chars: {repr(pre_ctx)}")
print(f"After `</script>` first 50 chars: {repr(post_ctx)}")
