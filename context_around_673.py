with open(r'core/templates/core/dashboard/upload_marks_excel.html', encoding='utf-8') as f:
    lines = f.readlines()

# Show exact content of lines 509-520 to verify parent form/group structure
print("=== Lines 509-520 (form and first form-group structure) ===")
for i, line in enumerate(lines[508:520], start=509):
    print(f"{i:4d}: {line}", end='')

print("\n=== Lines 591-677 (instructions-section and surrounding) ===")
for i, line in enumerate(lines[590:677], start=591):
    print(f"{i:4d}: {line}", end='')

print("\n=== Lines 673-680 (context at the close) ===")
for i, line in enumerate(lines[672:680], start=673):
    print(f"{i:4d}: {line}", end='')
