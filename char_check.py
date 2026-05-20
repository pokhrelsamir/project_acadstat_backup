with open(r'core\templates\core\dashboard\upload_marks_excel.html', encoding='utf-8') as f:
    text = f.read()
script_start = 28121
end_tag_pos = text.find('</script>', script_start)  # this is 37362
print("</script> at:", end_tag_pos)
print("Chars before and after positions 37355-37375:")
for i in range(37355, min(37375, len(text))):
    print(f"  {i}: [{text[i]!r}]")

print(f"\nWhat came out of extraction: text[start:end_tag_pos]")
extracted = text[script_start:end_tag_pos]
print(f"So last chars of extracted are:")
for i, c in enumerate(extracted[-20:], len(extracted)-19):
    print(f"  {i}: [{c!r}]")
