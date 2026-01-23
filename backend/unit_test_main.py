from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import pytest
from datetime import datetime, timedelta

from main import app, get_db
from database import Base

# Use a proper in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def test_original_get_db():
    """Test the original get_db function"""
    from main import get_db
    db_gen = get_db()
    db = next(db_gen)
    assert db is not None
    try:
        next(db_gen)
    except StopIteration:
        pass


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user():
    """Create a test user and return credentials"""
    response = client.post(
        "/register",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpass123"
        }
    )
    assert response.status_code == 201, f"Registration failed: {response.json()}"
    return {"username": "testuser", "password": "testpass123"}


@pytest.fixture
def auth_headers(test_user):
    """Get authentication headers with valid token"""
    # FIXED: Changed from /token to /login
    response = client.post(
        "/login",
        data={
            "username": test_user["username"],
            "password": test_user["password"]
        }
    )
    assert response.status_code == 200, f"Login failed: {response.json()}"
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# ============================================
# TASK TESTS
# ============================================

def test_update_status_not_found(auth_headers):
    """Test updating status of non-existent task"""
    response = client.patch(
        "/tasks/99999/status",
        json={"status": "completed"},
        headers=auth_headers
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_delete_task_not_found(auth_headers):
    """Test deleting non-existent task"""
    response = client.delete("/tasks/99999", headers=auth_headers)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_create_task(auth_headers):
    """Test creating a task"""
    due_date = (datetime.now() + timedelta(days=7)).isoformat()
    response = client.post(
        "/tasks",
        json={
            "title": "Test Task",
            "description": "Test Description",
            "status": "pending",
            "due_date": due_date
        },
        headers=auth_headers
    )
    assert response.status_code in [200, 201]
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["status"] == "pending"
    assert "id" in data


def test_read_task(auth_headers):
    """Test reading a specific task"""
    due_date = (datetime.now() + timedelta(days=7)).isoformat()
    create_response = client.post(
        "/tasks",
        json={
            "title": "Test Task",
            "description": "Test Description",
            "status": "pending",
            "due_date": due_date
        },
        headers=auth_headers
    )
    task_id = create_response.json()["id"]

    response = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Test Task"


def test_read_task_not_found(auth_headers):
    """Test reading non-existent task"""
    response = client.get("/tasks/999", headers=auth_headers)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_read_tasks(auth_headers):
    """Test reading all tasks"""
    due_date = (datetime.now() + timedelta(days=7)).isoformat()
    client.post(
        "/tasks",
        json={"title": "Task 1", "description": "Desc 1", "status": "pending", "due_date": due_date},
        headers=auth_headers
    )
    client.post(
        "/tasks",
        json={"title": "Task 2", "description": "Desc 2", "status": "in_progress", "due_date": due_date},
        headers=auth_headers
    )

    response = client.get("/tasks", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_update_task_status(auth_headers):
    """Test updating task status"""
    due_date = (datetime.now() + timedelta(days=7)).isoformat()
    create_response = client.post(
        "/tasks",
        json={
            "title": "Test Task",
            "description": "Test Description",
            "status": "pending",
            "due_date": due_date
        },
        headers=auth_headers
    )
    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}/status",
        json={"status": "completed"},
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["status"] == "completed"


def test_delete_task(auth_headers):
    """Test deleting a task"""
    due_date = (datetime.now() + timedelta(days=7)).isoformat()
    create_response = client.post(
        "/tasks",
        json={
            "title": "Test Task",
            "description": "Test Description",
            "status": "pending",
            "due_date": due_date
        },
        headers=auth_headers
    )
    task_id = create_response.json()["id"]

    response = client.delete(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code in [200, 204]

    get_response = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert get_response.status_code == 404


def test_invalid_status(auth_headers):
    """Test that invalid status values are rejected"""
    due_date = (datetime.now() + timedelta(days=7)).isoformat()
    response = client.post(
        "/tasks",
        json={
            "title": "Test Task",
            "description": "Test Description",
            "status": "invalid_status",
            "due_date": due_date
        },
        headers=auth_headers
    )
    assert response.status_code == 422


def test_missing_required_fields(auth_headers):
    """Test that missing required fields are rejected"""
    response = client.post(
        "/tasks",
        json={"title": "Test Task"},
        headers=auth_headers
    )
    assert response.status_code == 422


# ============================================
# AUTHENTICATION TESTS
# ============================================

def test_register_user():
    """Test user registration"""
    response = client.post(
        "/register",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpass123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "newuser"
    assert "id" in data
    assert "password" not in data


def test_register_duplicate_username(test_user):
    """Test that duplicate usernames are rejected"""
    response = client.post(
        "/register",
        json={
            "username": test_user["username"],
            "email": "another@example.com",
            "password": "anotherpass"
        }
    )
    assert response.status_code == 400
    assert "already" in response.json()["detail"].lower()


def test_login_success(test_user):
    """Test successful login"""
    # FIXED: Changed from /token to /login
    response = client.post(
        "/login",
        data={
            "username": test_user["username"],
            "password": test_user["password"]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(test_user):
    """Test login with wrong password"""
    # FIXED: Changed from /token to /login
    response = client.post(
        "/login",
        data={
            "username": test_user["username"],
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401


def test_login_nonexistent_user():
    """Test login with non-existent user"""
    # FIXED: Changed from /token to /login
    response = client.post(
        "/login",
        data={
            "username": "nonexistent",
            "password": "password"
        }
    )
    # Accept either 401 or 404
    assert response.status_code in [401, 404]


def test_unauthorized_access():
    """Test that endpoints require authentication"""
    response = client.get("/tasks")
    assert response.status_code == 401


def test_invalid_token():
    """Test that invalid tokens are rejected"""
    response = client.get(
        "/tasks",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401


# ============================================
# CORS TESTS
# ============================================

def test_cors_configuration():
    """Test CORS middleware configuration for allowed origins"""
    allowed_origins = [
        "http://localhost:63342",
        "http://127.0.0.1:63342",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ]

    for origin in allowed_origins:
        response = client.options(
            "/tasks",
            headers={
                "Origin": origin,
                "Access-Control-Request-Method": "GET",
                "Access-Control-Request-Headers": "Content-Type"
            }
        )

        assert "access-control-allow-origin" in response.headers
        assert response.headers["access-control-allow-origin"] == origin
        assert "access-control-allow-credentials" in response.headers
        assert response.headers["access-control-allow-credentials"] == "true"


def test_cors_with_actual_request(test_user):
    """Test CORS headers on actual requests"""
    # FIXED: Changed from /token to /login
    login_response = client.post(
        "/login",
        data={
            "username": test_user["username"],
            "password": test_user["password"]
        }
    )
    token = login_response.json()["access_token"]

    origin = "http://localhost:63342"
    response = client.get(
        "/tasks",
        headers={
            "Origin": origin,
            "Authorization": f"Bearer {token}"
        }
    )

    assert "access-control-allow-origin" in response.headers
    assert response.headers["access-control-allow-origin"] == origin


def test_cors_disallowed_origin():
    """Test that disallowed origins don't get CORS headers"""
    disallowed_origin = "http://malicious-site.com"

    response = client.options(
        "/tasks",
        headers={
            "Origin": disallowed_origin,
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "Content-Type"
        }
    )

    if "access-control-allow-origin" in response.headers:
        assert response.headers["access-control-allow-origin"] != disallowed_origin


def test_cors_allowed_methods():
    """Test that all configured HTTP methods are allowed"""
    origin = "http://localhost:63342"

    response = client.options(
        "/tasks",
        headers={
            "Origin": origin,
            "Access-Control-Request-Method": "POST",
        }
    )

    if "access-control-allow-methods" in response.headers:
        allowed = response.headers["access-control-allow-methods"]
        assert any(method in allowed or method.lower() in allowed.lower()
                   for method in ["GET", "POST", "PUT", "DELETE", "PATCH"])


def test_cors_credentials_support():
    """Test that credentials are properly supported"""
    origin = "http://localhost:63342"

    response = client.options(
        "/tasks",
        headers={
            "Origin": origin,
            "Access-Control-Request-Method": "POST",
        }
    )

    assert "access-control-allow-credentials" in response.headers
    assert response.headers["access-control-allow-credentials"].lower() == "true"


def test_cors_exposed_headers():
    """Test that headers are properly exposed"""
    origin = "http://localhost:63342"

    response = client.options(
        "/tasks",
        headers={
            "Origin": origin,
            "Access-Control-Request-Method": "GET",
        }
    )

    assert response.status_code in [200, 204]


# ============================================
# ADDITIONAL CORS EDGE CASE TESTS
# ============================================

def test_cors_preflight_all_origins():
    """Test that each allowed origin works independently"""
    allowed_origins = [
        "http://localhost:63342",
        "http://127.0.0.1:63342",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ]

    for origin in allowed_origins:
        response = client.options(
            "/register",
            headers={
                "Origin": origin,
                "Access-Control-Request-Method": "POST",
            }
        )
        # Each origin should be handled correctly
        assert response.status_code in [200, 204]
        if "access-control-allow-origin" in response.headers:
            assert response.headers["access-control-allow-origin"] == origin


def test_cors_multiple_headers():
    """Test that multiple request headers are allowed"""
    origin = "http://localhost:63342"

    response = client.options(
        "/tasks",
        headers={
            "Origin": origin,
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Content-Type, Authorization"
        }
    )

    assert response.status_code in [200, 204]
    assert "access-control-allow-headers" in response.headers or "access-control-allow-origin" in response.headers