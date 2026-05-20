with open(r'core\templates\core\dashboard\upload_marks_excel.html', encoding='utf-8') as f:
    text = f.read()
js_tag = '<script>\n        // Wait for DOM to be ready'
start = text.find(js_tag)
end = text.find('</script>', start)
js = text[start:end]

open_b = js.count('{')
close_b = js.count('}')
open_p = js.count('(')
close_p = js.count(')')

print('brace: open=%d, close=%d, diff=%d' % (open_b, close_b, open_b-close_b))
print('paren: open=%d, close=%d, diff=%d' % (open_p, close_p, open_p-close_p))

# Count function( openings  
open_positions = []
search = 0
while True:
    pos = js.find('function(', search)
    if pos < 0:
        break
    open_positions.append(pos)
    search = pos+1
print('\nfunction( at %d positions: %s' % (len(open_positions), open_positions))

# Count }); closures
close_positions = []
search = 0
while True:
    pos = js.find('});', search)
    if pos < 0:
        break
    close_positions.append(pos)
    search = pos+1
print('\nclose }); at %d positions (last 5): %s' % (len(close_positions), close_positions[-5:]))

# Comparison
print('\nComparison:')
print('  function( opens: %d' % len(open_positions))
print('  }); closes: %d' % len(close_positions))
print('  They should be equal. Are they? %s' % ('YES' if len(open_positions)==len(close_positions) else 'NO'))
