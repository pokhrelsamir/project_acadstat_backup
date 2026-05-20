import subprocess, sys

# Try to find node or npx
import shutil
node = shutil.which('node')
print("node found:", node)
npx = shutil.which('npx')
print("npx found:", npx)

if node:
    result = subprocess.run([node, '-e', 'require("acorn").parse(open("js_extracted.js").read())'],
                           capture_output=True, text=True, shell=True)
    print("stdout:", result.stdout[:200])
    print("stderr:", result.stderr[:200])
else:
    print("No node.js available, will check via manual pattern matching")

with open('js_extracted.js', encoding='utf-8') as f:
    js = f.read()

# Manual check
open_braces = js.count('{')
close_braces = js.count('}')
open_parens = js.count('(')
close_parens = js.count(')')
print(f"\nBraces balance: {{ = {open_braces}, }} = {close_braces}")
print(f"Parens balance: ( = {open_parens}, ) = {close_parens}")
print(f"Braces ok: {open_braces == close_braces}")
print(f"Parens ok: {open_parens == close_parens}")
