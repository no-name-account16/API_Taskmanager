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
print("\033[92mDIAGNOSTIC REPORT\033[0m")
print("=" * 60)
print(f"\nPython Version: {sys.version}")
print(f"Current Directory: {os.getcwd()}")
print(f"\nPython Files in current directory:")
for f in sorted(os.listdir('.')):
    if f.endswith('.py'):
        print(f"   {f}")

print("\n" + "=" * 60)
print("\033[92mTESTING PACKAGE IMPORTS\033[0m")
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
        print(f"{module:20s} - \033[92mINSTALLED\033[0m")
    except ImportError:
        print(f"{module:20s} - \033[91mMISSING\033[0m")
        failed_packages.append(install_cmd)

print("\n" + "=" * 60)
print("\033[92mTESTING LOCAL MODULE IMPORTS\033[0m")
print("=" * 60)

local_modules = ['database', 'models', 'schemas', 'authentication', 'db_interaction']

for module in local_modules:
    try:
        __import__(module)
        print(f"{module}.py - OK")
    except Exception as e:
        print(f"{module}.py - ERROR: {e}")

print("\n" + "=" * 60)
print("\033[92mTESTING MAIN.PY IMPORT\033[0m")
print("=" * 60)

try:
    import main
    print("\033[43m main.py imported successfully!\033[0m")
    print("\nYour server should work! Run:")
    print(" \033[92m  python -m uvicorn main:app --reload\033[0m")
except Exception as e:
    print(f"\033[91m main.py import FAILED!\033[0m")
    print(f"\nError: {e}")
    print(f"\nFull traceback:")
    import traceback
    traceback.print_exc()

if failed_packages:
    print("\n" + "=" * 60)
    print("\033[91mMISSING PACKAGES - RUN THIS:\033[0m")
    print("=" * 60)
    for cmd in failed_packages:
        print(f"  {cmd}")
    print("\nOr install all at once:")
    print(' pip install fastapi uvicorn sqlalchemy pydantic "python-jose[cryptography]" "passlib[bcrypt]" python-multipart email-validator ')

print("\n" + "=" * 60)

