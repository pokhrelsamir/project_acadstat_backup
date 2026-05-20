"""Find the DIV OPEN at indent=12 that starts at depth 4."""
with open(r'core/templates/core/dashboard/upload_marks_excel.html', encoding='utf-8') as f:
    lines = f.readlines()

# The form-card opens at indent 12 (line 465).
# After form-card, there should be 4 closes at 12, 8, 4 to close:
# form-card -> the indent-8 wrapper -> the indent-4 wrapper
# Then the next closing should be at indent 0 for </body>, </html>, etc.
# BEFORE </form>, those 4 outer divs should NOT close.

# Let's verify by counting how many div opens vs closes happen BEFORE form close
# vs AFTER form close

print("=== DIV STRUCTURE: BEFORE </form> at line 589 ===")
opens_before = 0
closes_before = 0
opens_list = []

for i, line in enumerate(lines):
    stripped = line.strip()
    lineno = i + 1
    if lineno >= 589:
        break
    if stripped.startswith('<div') and '>' in stripped:
        opens_before += 1
        opens_list.append(lineno)
    if stripped == '</div>':
        closes_before += 1

print("  Opens before form close:", opens_before)
print("  Closes before form close:", closes_before)
print("  Net before form close:", opens_before - closes_before)
print("  Open divs at line 589:", opens_before - closes_before)

print("\n=== DIV STRUCTURE: AFTER </form> at line 589 ===")
opens_after = 0
closes_after = 0
for i, line in enumerate(lines):
    lineno = i + 1
    if lineno <= 589:
        continue
    stripped = line.strip()
    if stripped.startswith('<div') and '>' in stripped:
        opens_after += 1
    if stripped == '</div>':
        closes_after += 1

print("  Opens after form close:", opens_after)
print("  Closes after form close:", closes_after)
print("  Closes in page body after form:", closes_after)

# Important insight: if form-card has 1 div of the form-header + form-body
# and </form> at line 589 closes, then the 4 remaining </div> at lines 673-676
# MUST be closing the SIBLINGS of form-card div for the HTML to be balanced.
# But the nesting tells us the BRANCH closes INSIDE the form-card.

# The mismatch: 
# - instructions-section opens at line 591 INSIDE form-card DIV at indent 12
# - This orphan instructions-section has NO corresponding </div> in the file
# because lines 673-676 close the NESTED parents of form-card, not instructions

print("\n=== KEY OBSERVATION ===")
print("instructions-section div opens at line 591 (inside form-card)")
print("There are 4 </div> closes at lines 673-676 (form-card ancestors)")
print("If these 4 closes just close the outer divs above form-card,")
print("THEN there is NO </div> corresponding to the instructions-section div!")
print()
print("That means instructions-section is unclosed / mis-nested.")
print("This structurally contaminates the DOM and probably DIVs the CSS cascade")
