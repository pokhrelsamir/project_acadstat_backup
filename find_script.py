with open(r'core\templates\core\dashboard\upload_marks_excel.html', encoding='utf-8') as f:
    text = f.read()
script_start_text = text.find('<script>\n        // Wait for DOM to be ready')
print(f"Script start at: {script_start_text}")
print(f"Script start context: {repr(text[script_start_text:script_start_text+50])}")

# What follows '<script>\n        // Wait for DOM to be ready'  
print(f"\nHTML content from <script> to {'</script>'} start (50 chars):")
print(repr(text[script_start_text:script_start_text+50]))

# What defines the border between handler body and outer closure
# show the exact HTML at position 28177
print(f"\nAt script_start+56 = {script_start_text+56}:")
print(repr(text[script_start_text+50:script_start_text+100]))

# Show all captured script lines
actual_end = text.find('\n    </script>', script_start_text) 
# Or the full 
actual_end2 = text.find('</script>', script_start_text)

print(f"\n</script> at position: {actual_end2}")
print(f"Script length from start+8 to end tag: {actual_end2 - script_start_text - 8}")

# Lines around the end
end_context = text[actual_end2-100:actual_end2+50]
print(f"\nContext around </script>:")
print(end_context)
print("repr:", repr(end_context))
