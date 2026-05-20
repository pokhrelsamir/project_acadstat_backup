#!/usr/bin/env python
"""
Setup script for teacher authentication system.
Run this after applying migrations to create sample teacher accounts.
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'academicsys.settings')

django.setup()

from django.core.management import execute_from_command_line

if __name__ == '__main__':
    print("Setting up teacher authentication system...")
    print("============================================")

    # Run migrations first
    print("1. Running migrations...")
    execute_from_command_line(['manage.py', 'migrate'])

    # Create sample teacher accounts
    print("\n2. Creating sample teacher accounts...")
    execute_from_command_line(['manage.py', 'create_teachers', '--create-sample'])

    print("\n3. Setup complete!")
    print("\nYou can now:")
    print("- Login as admin at /admin/ (create superuser if needed)")
    print("- Assign subjects and students to teachers via admin")
    print("- Login as teachers using their credentials")
    print("- Teachers will be redirected to their restricted dashboard")
    print("\nSample teacher accounts:")
    print("- teacher_math: password123")
    print("- teacher_science: password123")
    print("- teacher_cs: password123")