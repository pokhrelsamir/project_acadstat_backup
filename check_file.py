import os
path = r'core/templates/core/dashboard/upload_marks_excel.html'
print("File exists:", os.path.exists(path))
print("File size:", os.path.getsize(path) if os.path.exists(path) else "N/A")
