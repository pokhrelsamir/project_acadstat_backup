import os, sys, subprocess, time, urllib.request

os.environ.setdefault('DJANGO_SETTINGS_MODULE','academicsys.settings')

PORT = 18765
print(f'Starting server on 127.0.0.1:{PORT}...')
proc = subprocess.Popen(
    [sys.executable, 'manage.py', 'runserver', f'127.0.0.1:{PORT}', '--noreload'],
    stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd='.'
)
time.sleep(4)

print(f'Server PID: {proc.pid}')

# First: read any startup errors
stderr_data = b''
try:
    stderr_data = proc.stderr.read(4096)  # non-blocking
except:
    pass
if stderr_data:
    print('STARTUP STDERR:')
    print(stderr_data.decode(errors='replace'))

# Second: make the request and SERVER-SIDE trace stderr at the same time
print(f'\nRequesting http://127.0.0.1:{PORT}/download-excel-template/')
error_response = b''
try:
    req = urllib.request.Request(
        f'http://127.0.0.1:{PORT}/download-excel-template/',
        headers={'Accept': '*/*'}
    )
    import urllib.request
    resp = urllib.request.urlopen(req, timeout=10)
    body = resp.read()
    print(f'Status: {resp.status}')
    print(f'CT: {resp.headers.get("Content-Type")}')
    print(f'CD: {resp.headers.get("Content-Disposition")}')
    print(f'Body: {len(body)} bytes, header={body[:4]}')
except urllib.error.HTTPError as e:
    body = e.read()
    print(f'HTTP {e.code}')
    print(f'Body[:500]: {body.decode(errors="replace")[:500]}')
    # Slurp server stderr after the request
    time.sleep(1)
    try:
        post = proc.stderr.read()
        print('\n--- POST-REQUEST STDERR ---')
        print(post.decode(errors='replace')[-3000:])
    except:
        pass
finally:
    proc.terminate()
    try: proc.wait(timeout=5)
    except: proc.kill()
    print('\nServer terminated.')
