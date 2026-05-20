import os, sys, traceback, time
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'academicsys.settings')
import django; django.setup()

from core.views_excel import download_excel_template
from django.test import RequestFactory
from django.contrib.auth.models import User

# Simulate a request with ALL the same call stack as Vercel (ASGI-like)
rf = RequestFactory()
req = rf.get('/download-excel_template/')          # missing trailing slash
req.user = User.objects.get(id=25)

print('=== Test 1: `/download-excel_template/` (no trailing slash) ===')
try:
    resp = download_excel_template(req)
    print('Status:', resp.status_code)
except Exception as e:
    print('EXCEPTION:', type(e).__name__, ':', e)

# Test normal
req2 = rf.get('/download-excel-template/')
req2.user = User.objects.get(id=25)

print('\n=== Test 2: `/download-excel-template/` (correct trailing slash) ===')
t0 = time.time()
try:
    resp2 = download_excel_template(req2)
    dt = time.time() - t0
    print('Status:', resp2.status_code, f'(took {dt:.3f}s)')
except Exception as e:
    dt = time.time() - t0
    print('EXCEPTION:', type(e).__name__, ':', e, f'(took {dt:.3f}s)')
    traceback.print_exc()

# Test with WSGIHandler explicitly
print('\n=== Test 3: via WSGIApplication ===')
from django.core.handlers.wsgi import WSGIHandler
from io import BytesIO

class FakePath:
    def __init__(self, p): self.path = p
    def __str__(self): return self.path

environ = {
    'REQUEST_METHOD': 'GET',
    'PATH_INFO': '/download-excel-template/',
    'SERVER_NAME': '127.0.0.1',
    'SERVER_PORT': '8000',
    'HTTP_HOST': '127.0.0.1:8000',
    'HTTP_COOKIE': '',
    'wsgi.input': BytesIO(),
    'wsgi.errors': sys.stderr,
    'wsgi.url_scheme': 'http',
}

try:
    handler = WSGIHandler()
    response_status = []
    response_headers = []
    
    def start_response(status, headers):
        response_status.append(status)
        response_headers.extend(headers)
    
    r = handler(environ, start_response)
    body = b''
    for chunk in r:
        body += chunk
    print(f'Status line : {response_status[0]}')
    print(f'Headers:')
    for h in response_headers:
        print(f'  {h[0]}: {h[1]}')
    print(f'Body length: {len(body)} bytes')
    print(f'First bytes : {body[:8]}')
except Exception as e:
    print('WSGI EXCEPTION:', type(e).__name__, ':', e)
    traceback.print_exc()
