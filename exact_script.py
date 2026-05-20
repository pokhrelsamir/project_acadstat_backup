with open(r'core\templates\core\dashboard\upload_marks_excel.html', encoding='utf-8') as f:
    text = f.read()

script_start = 28121
script_end = 37362  # position of </script>

# Get the actual script content INCLUDING everything up to but not including </script>
actual_script = text[script_start:script_end]
print("Script content last 200 chars repr:")
print(repr(actual_script[-200:]))
print()
print("Script content total length:", len(actual_script))
print()
print("Character by character of last 20 chars:")
for i, c in enumerate(actual_script[-20:], len(actual_script)-19):
    print(f"  {i}: [{c!r}] U+{ord(c):04X}")
