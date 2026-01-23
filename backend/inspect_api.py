"""
Run this script to discover what your API expects for registration
Usage: python inspect_api.py
"""
from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)

print("=" * 80)
print("INSPECTING YOUR FASTAPI APPLICATION")
print("=" * 80)
print()

# Get OpenAPI schema
print("📋 Fetching OpenAPI Schema...")
openapi_response = client.get("/openapi.json")

if openapi_response.status_code == 200:
    openapi = openapi_response.json()

    # 1. Show all available endpoints
    print("\n" + "=" * 80)
    print("📍 AVAILABLE ENDPOINTS")
    print("=" * 80)
    if "paths" in openapi:
        for path, methods in openapi["paths"].items():
            for method, details in methods.items():
                print(f"  {method.upper():7} {path}")
                if "summary" in details:
                    print(f"          └─ {details['summary']}")

    # 2. Show UserCreate schema if it exists
    print("\n" + "=" * 80)
    print("👤 USER SCHEMAS")
    print("=" * 80)
    if "components" in openapi and "schemas" in openapi["components"]:
        schemas = openapi["components"]["schemas"]

        for schema_name in schemas.keys():
            if "user" in schema_name.lower() or "User" in schema_name:
                print(f"\n  📦 {schema_name}:")
                schema = schemas[schema_name]
                if "properties" in schema:
                    print("     Properties:")
                    for prop_name, prop_details in schema["properties"].items():
                        required = " (REQUIRED)" if "required" in schema and prop_name in schema["required"] else ""
                        prop_type = prop_details.get("type", "unknown")
                        print(f"       - {prop_name}: {prop_type}{required}")
                print(f"\n     Full Schema:")
                print(f"     {json.dumps(schema, indent=6)}")

    # 3. Show /register endpoint details
    print("\n" + "=" * 80)
    print("🔐 REGISTER ENDPOINT DETAILS")
    print("=" * 80)
    if "paths" in openapi and "/register" in openapi["paths"]:
        register_def = openapi["paths"]["/register"]
        if "post" in register_def:
            post_def = register_def["post"]
            print(f"\n  Summary: {post_def.get('summary', 'N/A')}")
            print(f"  Description: {post_def.get('description', 'N/A')}")

            if "requestBody" in post_def:
                print("\n  Request Body:")
                print(f"  {json.dumps(post_def['requestBody'], indent=4)}")

            if "responses" in post_def:
                print("\n  Responses:")
                for code, response in post_def["responses"].items():
                    print(f"    {code}: {response.get('description', 'N/A')}")

    # 4. Show Task schemas
    print("\n" + "=" * 80)
    print("📝 TASK SCHEMAS")
    print("=" * 80)
    if "components" in openapi and "schemas" in openapi["components"]:
        schemas = openapi["components"]["schemas"]

        for schema_name in schemas.keys():
            if "task" in schema_name.lower() or "Task" in schema_name:
                print(f"\n  📦 {schema_name}:")
                schema = schemas[schema_name]
                if "properties" in schema:
                    print("     Properties:")
                    for prop_name, prop_details in schema["properties"].items():
                        required = " (REQUIRED)" if "required" in schema and prop_name in schema["required"] else ""
                        prop_type = prop_details.get("type", "unknown")
                        print(f"       - {prop_name}: {prop_type}{required}")

else:
    print(f"❌ Could not fetch OpenAPI schema. Status: {openapi_response.status_code}")

# Test actual registration
print("\n" + "=" * 80)
print("🧪 TESTING REGISTRATION")
print("=" * 80)

test_cases = [
    ("Standard Format", {"username": "test1", "password": "testpass123"}),
    ("With Email", {"username": "test2", "email": "test@test.com", "password": "testpass123"}),
    ("With Full Name", {"username": "test3", "full_name": "Test User", "password": "testpass123"}),
]

for test_name, payload in test_cases:
    print(f"\n  Testing: {test_name}")
    print(f"  Payload: {payload}")
    response = client.post("/register", json=payload)
    print(f"  Status: {response.status_code}")
    if response.status_code in [200, 201]:
        print(f"  ✅ SUCCESS")
        print(f"  Response: {json.dumps(response.json(), indent=4)}")
    else:
        print(f"  ❌ FAILED")
        print(f"  Response: {json.dumps(response.json(), indent=4)}")

print("\n" + "=" * 80)
print("✅ INSPECTION COMPLETE")
print("=" * 80)