with open(r'core/templates/core/dashboard/upload_marks_excel.html', encoding='utf-8') as f:
    content = f.read()

# The teacher navigates to /upload-marks/ which shows the upload page
# The teacher selects an Excel file and clicks "Upload Marks"
# JS: uploadForm.addEventListener('submit', function(e) { ... fetch ... })
# fetch sends to `{% url "core:upload_marks_excel" %}`

# Let me verify the actual template URL will resolve correctly
# by checking what {% url "core:upload_marks_excel" %} expands to in a teacher context
# It's: /upload-marks/ (from core/urls.py path definition)

# The fetch sends POST to /upload-marks/ which maps to upload_marks_excel(request)
# In the view, 'excel_file' must be in request.FILES

# Let me look at the FORM visibility issue:
# is the submit button accessible?
# Check if the button has any structural issue

# From line-by-line analysis:
# - Line 568: <div class="form-actions"> (indent 20, inside form)
# - Line 569: <button type="submit" class="btn-primary" id="submitBtn" disabled>
# Line 576: </button>
# - Line 588: </div> (close form-actions)
# - Line 589: </form>

# This is all INSIDE the FORM tag (line 511 to 589). ✓ Correct for form submission.

# Now let me verify the file input is inside the form too
print("File input in form: %s" % ("Yes" if "<input type=" in content[content.find("<form"):content.find("</form>")] else "No"))

# Check the form closed properly with no extra tags
content_check = content  # full content
form_open = content.find('<form')
form_close = content.find('</form>', form_open)
after_form = form_close
next_tags_after_form = content[after_form:after_form+200]
next_tag_20 = content[after_form:after_form+20]
print("\nAfter </form>, first 150 chars:")
print(next_tags_after_form)

# Check what comes between form start and form end has correct content
from_pos = form_open
to_pos = form_close
form_body = content[from_pos:to_pos]
print("\nForm body first 100 chars:")
print(form_body[:100])
print("\nForm body last 100 chars:")
print(form_body[-100:])
