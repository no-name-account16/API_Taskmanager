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
    poolclass=StaticPool,  # Important for in-memory database
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def test_original_get_db():
    """Test the original get_db function - covers lines 25-29"""
    from main import get_db

    # Use the generator as FastAPI would
    db_gen = get_db()

    # Enter the context (get the db session)
    db = next(db_gen)
    assert db is not None

    # Exit the context (trigger finally block)
    try:
        next(db_gen)
    except StopIteration:
        pass  # Expected - generator is exhausted after finally


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
    # Create tables before each test
    Base.metadata.create_all(bind=engine)
    yield
    # Drop tables after each test
    Base.metadata.drop_all(bind=engine)


client = TestClient(app)


def test_update_status_not_found():
    """Test updating status of non-existent task - covers line 53"""
    response = client.patch("/tasks/99999/status", json={"status": "completed"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_delete_task_not_found():
    """Test deleting non-existent task - covers line 61"""
    response = client.delete("/tasks/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_create_task():
    due_date = (datetime.now() + timedelta(days=7)).isoformat()
    response = client.post(
        "/tasks",
        json={
            "title": "Test Task",
            "description": "Test Description",
            "status": "pending",
            "due_date": due_date
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["status"] == "pending"
    assert "id" in data


def test_read_task():
    due_date = (datetime.now() + timedelta(days=7)).isoformat()
    create_response = client.post(
        "/tasks",
        json={
            "title": "Test Task",
            "description": "Test Description",
            "status": "pending",
            "due_date": due_date
        }
    )
    task_id = create_response.json()["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Test Task"


def test_read_task_not_found():
    response = client.get("/tasks/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_read_tasks():
    due_date = (datetime.now() + timedelta(days=7)).isoformat()
    client.post(
        "/tasks",
        json={"title": "Task 1", "description": "Desc 1", "status": "pending", "due_date": due_date}
    )
    client.post(
        "/tasks",
        json={"title": "Task 2", "description": "Desc 2", "status": "in_progress", "due_date": due_date}
    )

    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_update_task_status():
    due_date = (datetime.now() + timedelta(days=7)).isoformat()
    create_response = client.post(
        "/tasks",
        json={
            "title": "Test Task",
            "description": "Test Description",
            "status": "pending",
            "due_date": due_date
        }
    )
    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}/status",
        json={"status": "completed"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "completed"


def test_delete_task():
    due_date = (datetime.now() + timedelta(days=7)).isoformat()
    create_response = client.post(
        "/tasks",
        json={
            "title": "Test Task",
            "description": "Test Description",
            "status": "pending",
            "due_date": due_date
        }
    )
    task_id = create_response.json()["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["detail"] == "Task deleted"

    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404


def test_invalid_status():
    """Test that invalid status values are rejected"""
    due_date = (datetime.now() + timedelta(days=7)).isoformat()
    response = client.post(
        "/tasks",
        json={
            "title": "Test Task",
            "description": "Test Description",
            "status": "invalid_status",  # This should fail
            "due_date": due_date
        }
    )
    assert response.status_code == 422


def test_missing_required_fields():
    """Test that missing required fields are rejected"""
    response = client.post(
        "/tasks",
        json={"title": "Test Task"}  # Missing status and due_date
    )
    assert response.status_code == 422



