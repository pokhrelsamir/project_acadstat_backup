with open(r'core\templates\core\dashboard\upload_marks_excel.html', encoding='utf-8') as f:
    text = f.read()

# Find the script block
start = text.find('<script>\n        // Wait for DOM to be ready')
print("script start:", start)
print("Context around script start:")
print(repr(text[start-10:start+30]))

# Search for various end markers
print("\nSearching for end markers:")
for marker in ['</script>', '</script>\n  </body>', '</script>\n</body>', '\n    </script>', '\n   </script>', '\n  </script>', '<\\script>', '\n</script>']:
    pos = text.find(marker, start)
    if pos >= 0:
        print(f"  Found '{marker}' at position {pos}")
        print(f"  Context: {repr(text[pos:pos+50])}")
        
# Find all occurrences of </script> type patterns in the file
print("\nAll occurrences of 'script' in file end:")
for m in ['script>', '<script', 'script-body']:
    occurrences = []
    idx = 0
    while True:
        idx = text.find(m, idx)
        if idx < 0:
            break
        occurrences.append(idx)
        idx += 1
    print(f"  '{m}': {occurrences}")
