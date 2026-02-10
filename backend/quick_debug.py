"""
Quick script to see what the registration error actually says
change the username and password   + email if user exits  
"""
from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)

print("=" * 80)
print("\033[92mDEBUGGING REGISTRATION ENDPOINT\033[0m")
print("=" * 80)
print()

# Test 1: Current format
print("\033[93mTest 1: Current format (username + password)\033[0m")
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
print("\033[93mTest 2: With email field\033[0m")
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
print("\033[93mTest 3: Checking available routes\033[0m")
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
    print("\033[92mCould not fetch OpenAPI schema\033[0m")

print()
print("=" * 80)