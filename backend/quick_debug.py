"""
Quick script to see what the registration error actually says
Save as quick_debug.py and run: python quick_debug.py
"""
from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)

print("=" * 80)
print("DEBUGGING REGISTRATION ENDPOINT")
print("=" * 80)
print()

# Test 1: Current format
print("Test 1: Current format (username + password)")
print("-" * 80)
response = client.post(
    "/register",
    json={
        "username": "testuser",
        "password": "testpass123"
    }
)
print(f"Status Code: {response.status_code}")
print(f"Response:")
print(json.dumps(response.json(), indent=2))
print()

# Test 2: With email
print("Test 2: With email field")
print("-" * 80)
response = client.post(
    "/register",
    json={
        "username": "testuser2",
        "email": "test@example.com",
        "password": "testpass123"
    }
)
print(f"Status Code: {response.status_code}")
print(f"Response:")
print(json.dumps(response.json(), indent=2))
print()

# Test 3: Check if endpoint exists
print("Test 3: Checking available routes")
print("-" * 80)
openapi = client.get("/openapi.json")
if openapi.status_code == 200:
    paths = openapi.json().get("paths", {})
    print("Available endpoints:")
    for path in paths.keys():
        print(f"  - {path}")

    if "/register" in paths:
        print("\n/register endpoint found!")
        print("Expected request body:")
        register_info = paths["/register"]
        if "post" in register_info:
            request_body = register_info["post"].get("requestBody", {})
            print(json.dumps(request_body, indent=2))
else:
    print("Could not fetch OpenAPI schema")

print()
print("=" * 80)