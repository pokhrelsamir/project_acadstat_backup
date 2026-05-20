with open(r'core\templates\core\dashboard\upload_marks_excel.html', encoding='utf-8') as f:
    text = f.read()

# Get the full script content (excluding the </script> tag itself)
script_start = 28121  # text.find('<script>\n...')
for marker in ['</script>', '<\\script>']:
    pos = text.find(marker, script_start)
    print(f"'{marker}' at {pos}: context = {repr(text[pos:pos+50])}")

actual_end = text.find('\n    </script>', script_start)
actual_end2 = text.find('</script>\n', script_start)
print(f"\nNewline-space-end at: {actual_end}")
print(f"Direct tag end at: {actual_end2}")

actual_script_content = text[script_start+8:actual_end]
print(f"\nActual script content length: {len(actual_script_content)}")
brace_balance = 0
paren_balance = 0
for c in actual_script_content:
    if c == '{': brace_balance += 1
    elif c == '}': brace_balance -= 1
    elif c == '(': paren_balance += 1
    elif c == ')': paren_balance -= 1

print(f"Brace balance: {brace_balance}")
print(f"Paren balance: {paren_balance}")

# Find if there are any unclosed things at the very end
if brace_balance != 0 or paren_balance != 0:
    final_brace = brace_balance
    final_paren = paren_balance
    lines = actual_script_content.split('\n')
    current_brace = current_paren = 0
    for i, line in enumerate(lines):
        for c in line:
            if c == '{': current_brace += 1
            elif c == '}': current_brace -= 1
            elif c == '(': current_paren += 1
            elif c == ')': current_paren -= 1
        if (brace_balance > 0 and current_brace == brace_balance) or \
           (brace_balance < 0 and current_brace == brace_balance) or \
           (paren_balance > 0 and current_paren == paren_balance) or \
           (paren_balance < 0 and current_paren == paren_balance):
            print(f"\nUnmatched found at line {i+1}: brace={current_brace}, paren={current_paren}")
            print(f"Content: {repr(line[:100])}")
            break
    
    # Show the last 30 lines of the script
    print("\nLast 30 lines of script:")
    for i, line in enumerate(lines[-30:], start=len(lines)-29):
        print(f"{i:4d}: {repr(line)[:100]}")
