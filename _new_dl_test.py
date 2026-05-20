import os, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE','academicsys.settings')
import django; django.setup()

from core.views_excel import download_excel_template
from django.test import RequestFactory
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()
u = User.objects.first()
print('User:', u)

client = RequestFactory()
req = client.get('/download-excel-template/')
req.user = u

resp = download_excel_template(req)
print('Status:', resp.status_code)
print('Content-Type:', resp.get('Content-Type'))
print('Content-Disposition:', resp.get('Content-Disposition'))
print('Content-Length:', resp.get('Content-Length'))
body = resp.content if hasattr(resp, 'content') else b''.join(resp)
print('Body length:', len(body) if body else 'unknown')
print('Starts with PK:', body[:2] == b'PK' if body else 'N/A')
