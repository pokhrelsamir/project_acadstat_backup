with open(r'core\templates\core\dashboard\upload_marks_excel.html', encoding='utf-8') as f:
    lines = f.readlines()
# Show lines 855-865 with explicit context to find missing close
print("=== FINAL PART OF JS IN HTML FILE ===")
for i, line in enumerate(lines[854:865], start=855):
    print(f"{i:4d}: {repr(line)}")
print()
print("Line 863 is '</script>' on HTML line 863 (the script should have ended earlier)")
print()
print("This confirms: the JS closes at line 861 with ');' closing the submit handler,")
print("but there is NO ');' to close the DOMContentLoaded event listener.")
print("Lines 862-863 are:")
print(f"  862: {repr(lines[861])}")
print(f"  863: {repr(lines[862])}")
