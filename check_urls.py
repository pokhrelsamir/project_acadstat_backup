import re

with open(r'C:\Users\poksa\Desktop\abc\core\urls.py', encoding='utf-8') as f:
    urls_text = f.read()
names = sorted(set(re.findall(r"name='(\w+)'", urls_text)))
dups = [x for x in names if names.count(x) > 1]
print(f"URL names ({len(names)}):")
for n in sorted(names):
    print(f"  {n}")
if dups:
    print(f"\nDUPLICATES: {set(dups)}")
else:
    print("\nNo duplicates — OK")
