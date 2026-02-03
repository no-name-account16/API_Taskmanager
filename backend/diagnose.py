"""
Diagnostic script to find import issues
Run this: python diagnose.py

If there are any problems with the code - run the diagnose.py and the result should show like below

  database.py - OK
  models.py - OK
  schemas.py - OK
  authentication.py - OK
  db_interaction.py - OK

============================================================
TESTING MAIN.PY IMPORT
============================================================
main.py imported successfully!

   Your server should work! Run:
   python -m uvicorn main:app --reload

"""


import sys
import os

print("=" * 60)
print("DIAGNOSTIC REPORT")
print("=" * 60)
print(f"\nPython Version: {sys.version}")
print(f"Current Directory: {os.getcwd()}")
print(f"\nPython Files in current directory:")
for f in sorted(os.listdir('.')):
    if f.endswith('.py'):
        print(f"   {f}")

print("\n" + "=" * 60)
print("TESTING PACKAGE IMPORTS")
print("=" * 60)

# Test each package individually
packages_to_test = [
    ('fastapi', 'pip install fastapi'),
    ('uvicorn', 'pip install uvicorn'),
    ('sqlalchemy', 'pip install sqlalchemy'),
    ('pydantic', 'pip install pydantic'),
    ('jose', 'pip install python-jose[cryptography]'),
    ('passlib', 'pip install passlib[bcrypt]'),
]

failed_packages = []

for module, install_cmd in packages_to_test:
    try:
        __import__(module)
        print(f"{module:20s} - INSTALLED")
    except ImportError:
        print(f"{module:20s} - MISSING")
        failed_packages.append(install_cmd)

print("\n" + "=" * 60)
print("TESTING LOCAL MODULE IMPORTS")
print("=" * 60)

local_modules = ['database', 'models', 'schemas', 'authentication', 'db_interaction']

for module in local_modules:
    try:
        __import__(module)
        print(f"{module}.py - OK")
    except Exception as e:
        print(f"{module}.py - ERROR: {e}")

print("\n" + "=" * 60)
print("TESTING MAIN.PY IMPORT")
print("=" * 60)

try:
    import main
    print("main.py imported successfully!")
    print("\nYour server should work! Run:")
    print("   python -m uvicorn main:app --reload")
except Exception as e:
    print(f"main.py import FAILED!")
    print(f"\nError: {e}")
    print(f"\nFull traceback:")
    import traceback
    traceback.print_exc()

if failed_packages:
    print("\n" + "=" * 60)
    print("MISSING PACKAGES - RUN THIS:")
    print("=" * 60)
    for cmd in failed_packages:
        print(f"  {cmd}")
    print("\nOr install all at once:")
    print('  pip install fastapi uvicorn sqlalchemy pydantic "python-jose[cryptography]" "passlib[bcrypt]" python-multipart email-validator')

print("\n" + "=" * 60)

