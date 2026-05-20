with open(r'core/templates/core/dashboard/upload_marks_excel.html', encoding='utf-8') as f:
    lines = f.readlines()

# Check for any button or input that might be inactive
print("=== KEY INTERACTIVE ELEMENTS ===")
for i, line in enumerate(lines, 1):
    stripped = line.strip()
    if ('<button' in stripped or '<input' in stripped or '<select' in stripped or
        '<form' in stripped):
        print(f"  {i:4d}: {stripped[:90]}")

print("\n=== BUTTON DISABLED/DISPLAY STATES ===")
for i, line in enumerate(lines, 1):
    if 'disabled' in line or 'display:none' in line.lower() or 'visibility' in line.lower():
        stripped = line.strip()
        print(f"  {i:4d}: {stripped[:80]}")
