import os, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE','academicsys.settings')
import django; django.setup()

from core.views_excel import download_excel_template
from django.test import RequestFactory
from django.contrib.auth import get_user_model
from core.models import Teacher, Subject, Student

User = get_user_model()

# Test 1: admin/superuser
u_admin = User.objects.filter(is_superuser=True).first()
print('=== Admin user ===')
print('username:', u_admin)
print('is_superuser:', u_admin.is_superuser)

rf = RequestFactory()
req = rf.get('/download-excel-template/')
req.user = u_admin

try:
    resp = download_excel_template(req)
    print('Status:', resp.status_code)
    print('CD:', resp.get('Content-Disposition'))
    print('Length:', resp.get('Content-Length'))
    body = resp.content if hasattr(resp, 'content') else b''.join(resp)
    print('Body:', len(body), 'bytes')
except Exception as e:
    import traceback; traceback.print_exc()

# Test 2: a regular teacher
t = Teacher.objects.first()
if t:
    print('\n=== Teacher:', t.first_name, t.last_name, '===')
    print('subjects:', t.subjects.count(), 'students:', t.students.count())
    
    req2 = rf.get('/download-excel-template/')
    req2.user = t.user
    try:
        resp2 = download_excel_template(req2)
        print('Status:', resp2.status_code)
        body2 = resp2.content if hasattr(resp2, 'content') else b''.join(resp2)
        print('Body:', len(body2), 'bytes')
    except Exception as e:
        import traceback; traceback.print_exc()
