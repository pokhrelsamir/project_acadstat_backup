with open(r'core\templates\core\dashboard\upload_marks_excel.html', encoding='utf-8') as f:
    text = f.read()

# Find ALL occurrences of </script> in the file
positions = []
search_from = 0
while True:
    pos = text.find('</script>', search_from)
    if pos < 0:
        break
    positions.append(pos)
    search_from = pos + 1

print(f"Found {len(positions)} occurrences of '</script>':")
for pos in positions:
    # Show context
    ctx = text[pos:pos+50]
    print(f"  At position {pos}: {repr(ctx[:80])}")

# Now find inline script start
script_start_marker = '<script>'
for marker in ['<script>\n        // Wait for DOM']:
    start_pos = text.find(marker)
    print(f"\nScript start marker '{marker[:30]}...' at: {start_pos}")
    
    print("Only position where '<script>' + newlines + Wait for DOM")
    # Enumerate all <script> locations
    all_script_starts = []
    s = 0
    while True:
        p = text.find('<script>', s)
        if p < 0: break
        all_script_starts.append(p)
        s = p + 1
    print(f"\nAll '<script>' positions: {all_script_starts}")
    print("\nWhich one is the inline JS?")
    for p in all_script_starts:
        ctx = text[p:p+100]
        if 'DOMContentLoaded' in ctx:
            print(f"  <<< INLINE JS at {p}: {repr(ctx[:80])}")
        
        else:
            print(f"  External script at {p}: {repr(ctx[:60])}")
