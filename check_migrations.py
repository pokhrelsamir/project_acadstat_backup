#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'academicsys.settings')
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    # Check django_migrations table
    cursor.execute("SELECT * FROM django_migrations WHERE app='core' ORDER BY applied")
    rows = cursor.fetchall()
    print("Applied migrations for 'core':")
    for row in rows:
        print(f"  {row[1]} - {row[2]}")

print("\nAll tables:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
for row in cursor.fetchall():
    print(f"  {row[0]}")
