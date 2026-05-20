with open('check_js.py', encoding='utf-8') as f:
    text = f.read()
with open('js_extracted.js', encoding='utf-8') as f:
    js_text = f.read()

# Re-find the actual end position
start = text.find('<script>\n        // Wait for DOM to be ready')
print("searching for end markers:")
print("  find '</script>\\n   </body>':", text.find('</script>\n   </body>', start))
print("  find '</script>':", text.find('</script>', start))
print("  find '</scrip':", text.find('</scrip', start))
print("  find '\\n    </script>':", text.find('\n    </script>', start))
print("  find '\\n   </script>':", text.find('\n   </script>', start))
print()

# Show what comes after the extracted JS ends
js_end = js_text[-50:]
print("JS extraction ends with:", repr(js_end))
# Check if that's actually in the original
idx = text.find(js_end.strip())
if idx >= 0:
    context = text[idx:idx+100]
    print("Found end context in original. Next 100 chars:")
    print(repr(context))
    # Print original lines after this
    full_pos = idx + len(js_end.strip())
    print("Text AFTER extracted end:", repr(text[full_pos:full_pos+200]))
