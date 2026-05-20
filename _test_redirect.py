import os, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE','academicsys.settings')
import django; django.setup()

from django.test import Client
from django.conf import settings

print('ALLOWED_HOSTS:', settings.ALLOWED_HOSTS)
print('DEBUG:', settings.DEBUG)

# Test with exact same headers a browser sends from 127.0.0.1:8000
client = Client(HTTP_HOST='127.0.0.1:8000')

from django.contrib.auth.models import User
u = User.objects.get(id=25)
client.force_login(u)

# Test the download endpoint
r = client.get('/download-excel-template/')
print(f'\nGET /download-excel-template/  status={r.status_code}')
print(f'  CT: {r.get("Content-Type","MISSING")}')
print(f'  CD: {r.get("Content-Disposition","MISSING")}')
print(f'  CL: {r.get("Content-Length","MISSING")}')
print(f'  body bytes: {len(r.content)}')

if r.status_code == 200:
    print(f'  body starts: {r.content[:16]}')
    print(f'  valid zip/ooxml: {r.content[:2] == b"PK"}')
elif r.status_code in (301, 302):
    print(f'  REDIRECT to: {r.get("Location","unknown")}')
    print(f'  Full response headers:')
    for h,v in r.items():
        print(f'    {h}: {v}')
