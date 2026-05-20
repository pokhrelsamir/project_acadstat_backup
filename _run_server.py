"""
Minimal reproducible test: start the dev server, hit the endpoint
directly from command line so we can catch the exact traceback.
"""
import os, sys, threading, time, urllib.request

os.environ.setdefault('DJANGO_SETTINGS_MODULE','academicsys.settings')
import django; django.setup()
from django.core.management import call_command

# Pin the port
PORT = 18764

print(f'Starting Django dev server on port {PORT}...')
def run_server():
    from django.core.servers.basehttp import run
    import socketserver
    from django.core.handlers.wsgi import WSGIHandler
    wsgi_handler = WSGIHandler()
    httpd = socketserver.TCPServer(('127.0.0.1', PORT), 
                                    type('Handler', (socketserver.BaseRequestHandler,), 
                                         {'handle': lambda self: None}))
    from wsgiref.simple_server import make_server
    httpd2 = make_server('127.0.0.1', PORT, wsgi_handler)
    httpd2.serve_forever()

# Use subprocess instead
import subprocess
server = subprocess.Popen(
    [sys.executable, 'manage.py', 'runserver', f'127.0.0.1:{PORT}', '--noreload'],
    stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd='.'
)
print(f'Server PID: {server.pid}')
time.sleep(3)

print('\nProbing server with urllib...')
try:
    req = urllib.request.Request(
        f'http://127.0.0.1:{PORT}/download-excel-template/',
        headers={'Accept': 'text/html,*/*'},
    )
    resp = urllib.request.urlopen(req, timeout=10)
    print(f'Status: {resp.status}')
    print(f'CT: {resp.headers.get("Content-Type")}')
    print(f'CD: {resp.headers.get("Content-Disposition")}')
    body = resp.read()
    print(f'Body: {len(body)} bytes')
    print(f'First bytes: {body[:8]}')
except urllib.error.HTTPError as e:
    print(f'HTTP Error {e.code}: {e.read().decode()[:500]}')
    # Try to get traceback from server stderr
    try:
        server_stderr = server.stderr.read().decode()
        if server_stderr:
            print('--- Server stderr ---')
            print(server_stderr[-2000:])
    except:
        pass
except Exception as e:
    print(f'Error: {type(e).__name__}: {e}')
finally:
    server.terminate()
    server.wait(timeout=3)
    print('\nServer stopped.')
