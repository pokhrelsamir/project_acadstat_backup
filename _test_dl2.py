import os, sys, traceback
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'academicsys.settings')
import django; django.setup()

from core.views_excel import _build_sheet, TERMINAL_SHEETS
import openpyxl
from io import BytesIO
from django.http import HttpResponse

teacher = None

wb = openpyxl.Workbook()
wb.remove(wb.active)
for sheet_name in TERMINAL_SHEETS:
    _build_sheet(wb, sheet_name, teacher)

bio = BytesIO()
wb.save(bio)
expected = bio.getvalue()
print('Workbook file size:', len(expected), 'bytes')
print('Workbook header:', expected[:4])

# save via HttpResponse
response = HttpResponse(
    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)
response['Content-Disposition'] = 'attachment; filename="bulk_marks_upload_template.xlsx"'

try:
    wb.save(response)
    print('wb.save(response) succeeded')
except Exception as e:
    print('wb.save(response) FAILED:', e)
    sys.exit(1)

# iterate to get content
all_chunks = []
total = 0
for chunk in response:
    if chunk:
        total += len(chunk)
        all_chunks.append(chunk)
actual = b''.join(all_chunks)
print('Actual body size:', total, 'bytes')
print('Match WB size:', total == len(expected))
print('Actual header:', actual[:4])
print('Valid ZIP/PK:', actual[:2] == b'PK')
print()

# Test the download view directly
from core.views_excel import download_excel_template
from django.test import RequestFactory
from django.contrib.auth.models import User

u = User.objects.all().first()
if not u:
    print('No user in DB! Creating test user...')
    u = User.objects.create_superuser('test500', '', 'test@test.com', password='test')
    
print('Using user:', u.username)

rf = RequestFactory()
req = rf.get('/download-excel-template/')
req.user = u

print('\n=== download_excel_template() response ===')
try:
    resp = download_excel_template(req)
    print('Status:', resp.status_code)
    print('Type:', type(resp).__name__)
    print('Content-Type:', resp.get('Content-Type'))
    print('Content-Disposition:', resp.get('Content-Disposition'))
    print('Body (iter):', sum(len(c) for c in resp), 'bytes')
    body = b''.join(c for c in resp if c)
    print('Body len:', len(body))
    print('Is ZIP:', body[:2] == b'PK')
    print('First 8:', body[:8])
except Exception as e:
    print('CAUGHT:', type(e).__name__, ':', e)
    traceback.print_exc()
