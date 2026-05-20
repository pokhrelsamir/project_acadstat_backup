with open(r'core\templates\core\dashboard\upload_marks_excel.html', encoding='utf-8') as f:
    text = f.read()

js_tag = '<script>\n        // Wait for DOM to be ready'
start = text.find(js_tag)
end = text.find('</script>', start)

print("Script start at: %d, end at: %d" % (start, end))
print("Last 100 chars of JS body:")
print(repr(text[end-100:end]))

# What's just before </script> in the HTML
before_end = end - 20
print("\nContext 20 chars before </script>:")
for i in range(max(0,before_end-30), end+30):
    print("%5d: [%s]" % (i, repr(text[i])))
