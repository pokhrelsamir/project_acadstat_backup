with open('js_extracted.js', encoding='utf-8') as f:
    text = f.read()

# Strip <script> opening and </script> closing tags
# Find the actual JS body start (after <script>\n)
start_tag_end = text.find('\n\n        // Wait for DOM to be ready')
# Find </script>
end_tag_start = text.rfind('</script>')
js_body = text[start_tag_end:end_tag_start]

brace_balance = 0
paren_balance = 0
max_brace = 0
max_brace_line = 0
max_paren = 0
max_paren_line = 0
anomalies = []
brace_lines = paren_lines = 0

with open('brace_results3.txt', 'w', encoding='utf-8') as out:
    out.write(f"JS body length: {len(js_body)}\n")
    out.write(f"JS body starts with: {js_body[:50]!r}\n")
    out.write(f"JS body ends with: {js_body[-50:]!r}\n\n")

    lines = js_body.split('\n')
    for i, line in enumerate(lines, 1):
        old_brace = brace_balance
        old_paren = paren_balance
        for c in line:
            if c == '{': brace_balance += 1
            elif c == '}': brace_balance -= 1
            elif c == '(': paren_balance += 1
            elif c == ')': paren_balance -= 1
        if brace_balance > max_brace:
            max_brace = brace_balance
            max_brace_line = i
        if paren_balance > max_paren:
            max_paren = paren_balance
            max_paren_line = i
        if brace_balance != 0 or paren_balance != 0:
            out.write(f"Line {i}: brace {old_brace:+d}->{brace_balance:+d}, paren {old_paren:+d}->{paren_balance:+d} | {line[:80]}\n")

    out.write(f"\nFinal brace balance: {brace_balance}\n")
    out.write(f"Final paren balance: {paren_balance}\n")
    out.write(f"Max brace depth: {max_brace} (line {max_brace_line})\n")
    out.write(f"Max paren depth: {max_paren} (line {max_paren_line})\n")

print("Wrote results to brace_results3.txt")
