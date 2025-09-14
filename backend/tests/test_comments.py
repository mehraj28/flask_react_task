# backend/tests/test_comments.py

import pytest
from app import create_app, db
from models import Task, Comment

# -----------------------------
# Fixtures
# -----------------------------
@pytest.fixture
def app():
    """
    Create and configure a new app instance for each test,
    using an in-memory SQLite database.
    """
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.app_context():
        db.create_all()  # create tables
        yield app
        db.session.remove()
        db.drop_all()  # drop tables after test

@pytest.fixture
def client(app):
    """Return a test client for the app."""
    return app.test_client()

# -----------------------------
# Test Cases
# -----------------------------

def test_create_task_and_comment(client):
    # -----------------------------
    # Create Task
    # -----------------------------
    res = client.post("/api/tasks", json={"title": "Test Task"})
    assert res.status_code == 201
    task_data = res.get_json()
    assert "id" in task_data
    task_id = task_data["id"]

    # -----------------------------
    # Add Comment
    # -----------------------------
    res = client.post(f"/api/tasks/{task_id}/comments", json={"content": "First Comment"})
    assert res.status_code == 201
    comment_data = res.get_json()
    assert comment_data["content"] == "First Comment"
    assert "id" in comment_data
    comment_id = comment_data["id"]

    # -----------------------------
    # Edit Comment
    # -----------------------------
    res = client.put(f"/api/comments/{comment_id}", json={"content": "Updated Comment"})
    assert res.status_code == 200
    updated = res.get_json()
    assert updated["content"] == "Updated Comment"

    # -----------------------------
    # Delete Comment
    # -----------------------------
    res = client.delete(f"/api/comments/{comment_id}")
    assert res.status_code == 200
    assert res.get_json()["message"] == "Comment deleted"

def test_task_list_and_comments_empty(client):
    # Initially, the database should have no tasks
    res = client.get("/api/tasks")
    assert res.status_code == 200
    assert res.get_json() == []

def test_task_list_after_creation(client):
    # Create a task
    client.post("/api/tasks", json={"title": "Sample Task"})
    res = client.get("/api/tasks")
    tasks = res.get_json()
    assert res.status_code == 200
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Sample Task"
    assert tasks[0]["description"] is None
