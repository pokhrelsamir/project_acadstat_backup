with open('js_extracted.js', encoding='utf-8') as f:
    text = f.read()
print("File length:", len(text))
print("Last 300 chars:")
print(repr(text[-300:]))
print()
print("Looking for </script> or /script:")
idx = text.find('</script>')
print("  </script> at", idx)
idx = text.find('/script>')
print("  /script> at", idx)

# Count occurrences of </script>
print("  rfind('</script>'):", text.rfind('</script>'))
print("  Contains '</script>':", '</script>' in text)
print("  Ends with '>':", text[-5:])
print("  Contains</scrip:", text.rfind('</scrip'))
print("  Contains <scpt(:", text.rfind('<scrip('))
