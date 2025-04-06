from idlelib.rpc import response_queue

from fastapi.testclient import TestClient
from main import app  # Import your FastAPI app

client = TestClient(app)  # Simulate API requests

def test_read_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Expecting a list of users

def test_create_user():
    new_user = {"username": "test_user", "email": "test@gmail.com"}
    response = client.post("/users/", json=new_user)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == new_user["username"]
    assert data["email"] == new_user["email"]
    assert "id" in data

def test_create_user_username():
    new_user = {"username": "", "email": ""}
    response = client.post("/users/", json=new_user)
    assert response.status_code == 422
    data = response.json()
    assert data["detail"] == "Username can't be empty!"

def test_read_user():
    response = client.get("/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "test_user"
    assert data["email"] == "test@gmail.com"

def test_user_not_found():
    response = client.get("/users/555")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User not found"

def test_update_user():
    update_user = {"username": "test_update", "email": "test_update@gmail.com"}
    response = client.put("/users/1", json=update_user)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "test_update"
    assert data["email"] == "test_update@gmail.com"

def test_update_user_not_found():
    update_user = {"username": "test_update", "email": "test_update@gmail.com"}
    response = client.put("/users/4738", json=update_user)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User not found"

def test_update_user_username_empty():
    update_user = {"username": "", "email": "test_update@gmail.com"}
    response = client.put("/users/1", json=update_user)
    assert response.status_code == 422
    data = response.json()
    assert data["detail"] == "Username can't be empty!"

def test_delete_user():
    response = client.delete("/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["detail"] == "User deleted"

def test_delete_user_not_found():
    response = client.delete("/users/1")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User not found"

def test_create_todo():
    new_user = {"username": "test_user", "email": "test@gmail.com"}
    client.post("/users/", json=new_user)
    new_todo = {"title": "test_todo", "description": "test description", "status": "Pending", "priority": "Medium", "user_id": 1}
    response = client.post("/todos/", json=new_todo)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == new_todo["title"]
    assert data["description"] == new_todo["description"]
    assert data["status"] == new_todo["status"]
    assert data["priority"] == new_todo["priority"]
    assert data["user_id"] == new_todo["user_id"]

def test_create_todo_empty_title():
    new_todo = {"title": "", "description": "test description", "status": "Pending", "priority": "Medium", "user_id": 1}
    response = client.post("/todos/", json=new_todo)
    assert response.status_code == 422
    data = response.json()
    assert data["detail"] == "Title can't be empty!"

def test_create_todo_user_not_found():
    new_todo = {"title": "test_todo", "description": "test description", "status": "Pending", "priority": "Medium", "user_id": 345}
    response = client.post("/todos/", json=new_todo)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User by this id is not found!"

