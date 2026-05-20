import os, sys, traceback
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'academicsys.settings')
import django; django.setup()

# CATCH-ALL: uncaught exceptions
from django.core.handlers import base
orig_handle = base.BaseHandler.handle_uncaught_exception
def traced_uncaught(request, resolver, exc_info):
    print(f"\n=== UNCAUGHT EXCEPTION at {request.path} ===")
    traceback.print_exception(*exc_info)
    return orig_handle(request, resolver, exc_info)
base.BaseHandler.handle_uncaught_exception = traced_uncaught

# Wrap the view itself
import core.views_excel as vem
orig_view = vem.download_excel_template
def wrapped(req):
    print('\n>>> download_excel_template CALLED')
    print('>>> user:', req.user)
    print('>>> path:', req.path)
    try:
        r = orig_view(req)
        print('>>> returned:', r.status_code, type(r).__name__)
        return r
    except Exception as e:
        print('>>> EXCEPTION in view:', type(e).__name__, ':', e)
        traceback.print_exc()
        raise
vem.download_excel_template = wrapped

# Full request
from django.test import Client
from django.contrib.auth.models import User
u = User.objects.get(id=25)
client = Client(HTTP_HOST='127.0.0.1:8000', HTTP_USER_AGENT='Chrome/122')
client.force_login(u)

print('=== GET /download-excel-template/ ===')
r = client.get('/download-excel-template/')
print('\nResponse:', r.status_code, type(r).__name__)
if r.status_code == 200:
    print('CT:', r.get('Content-Type','n/a'))
    print('CD:', r.get('Content-Disposition','n/a'))
    print('bytes:', len(r.content))
    print('header bytes:', r.content[:8])
    # Verify WB is full/valid
    import zipfile
    from io import BytesIO
    z = zipfile.ZipFile(BytesIO(r.content))
    print('zip entries:', len(z.namelist()))
    print('sample names:', z.namelist()[:4])
else:
    print('Response[:400]:', r.content.decode(errors='replace')[:400])
