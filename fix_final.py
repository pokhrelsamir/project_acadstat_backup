with open(r'core\templates\core\dashboard\upload_marks_excel.html', encoding='utf-8') as f:
    lines = f.readlines()

# Current line 860 (0-indexed 859) is the single merged line:
# '                    });\\n                });\\n            });\\n    </script>\n'
# We need to replace it with THREE proper separate lines + the closing </script> line

start_line_num = 860  # 1-indexed, current merged line
start_idx = start_line_num - 1  # 0-indexed

print("BEFORE - line 860:", repr(lines[start_idx]))
print("Total lines BEFORE:", len(lines))
print()

# Replace line 860 with 4 proper separate lines
lines[start_idx] = '                    });\n'
lines.insert(start_idx + 1, '                });\n')   # was part of the merged line  
lines.insert(start_idx + 2, '            });\n')       # was the missing `);` part
lines.insert(start_idx + 3, '    </script>\n')  

print("AFTER (lines 858-864):")
with open(r'core\templates\core\dashboard\upload_marks_excel.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)

with open(r'core\templates\core\dashboard\upload_marks_excel.html', encoding='utf-8') as f:
    new_lines = f.readlines()

for i, line in enumerate(new_lines[857:866], start=858):
    print(f"{i:4d}: {repr(line)}")
print(f"Total lines: {len(new_lines)}")

# HTML content balance check
text = ''.join(new_lines)
script_start = text.find('<script>\n        // Wait for DOM to be ready')
end_pos = text.find('</script>', script_start)
js_body = text[script_start:end_pos]
brace_bp = paren_bp = 0
for c in js_body:
    if c == '{': brace_bp += 1
    elif c == '}': brace_bp -= 1
    elif c == '(': paren_bp += 1
    elif c == ')': paren_bp -= 1
print(f"\nBrace balance: {brace_bp} (expected: 0)")
print(f"Paren balance: {paren_bp} (expected: 0)")
print(f"Script ends with: {repr(js_body[-50:])}")
