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

def test_get_all_todos():
    response = client.get("/todos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_todo_by_id():
    response = client.get("/todos/1")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "test_todo"
    assert data["description"] == "test description"
    assert data["status"] == "Pending"
    assert data["priority"] == "Medium"
    assert data["user_id"] == 1

def test_get_todo_by_id_not_found():
    response = client.get("/todos/4343")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Todo not found"

def test_update_todo():
    new_todo = {"title": "test_todo_update", "description": "test description update", "status": "Completed", "priority": "Low", "user_id": 1}
    response = client.put("/todos/1", json= new_todo)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == new_todo["title"]
    assert data["description"] == new_todo["description"]
    assert data["status"] == new_todo["status"]
    assert data["priority"] == new_todo["priority"]

def test_update_todo_not_found():
    new_todo = {"title": "test_todo_update", "description": "test description update", "status": "Completed", "priority": "Low", "user_id": 1}
    response = client.put("/todos/34324", json=new_todo)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Todo not found"

def test_update_todo_empty_title():
    new_todo = {"title": "", "description": "test description update", "status": "Completed", "priority": "Low", "user_id": 1}
    response = client.put("/todos/1", json=new_todo)
    assert response.status_code == 422
    assert response.json()["detail"] == "title can't be empty!"

def test_update_todo_user_not_found():
    new_todo = {"title": "test_todo_update", "description": "test description update", "status": "Completed", "priority": "Low", "user_id": 231321}
    response = client.put("/todos/1", json=new_todo)
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_delete_todo():
    response = client.delete("/todos/1")
    assert response.status_code == 200
    assert response.json()["detail"] == "Todo deleted"

def test_delete_todo_not_found():
    response = client.delete("/todos/12323")
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"

def test_get_todos_by_user():
    new_todo = {"title": "test_todo", "description": "test description", "status": "Pending", "priority": "Medium", "user_id": 1}
    client.post("/todos/", json=new_todo)
    response = client.get("/todos/todobyuser/1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_todos_by_user_not_found():
    response = client.get("/todos/todobyuser/32324")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_get_todos_by_user_no_todos():
    new_user = {"username": "test_user2", "email": "test2@gmail.com"}
    client.post("/users/", json=new_user)
    response = client.get("/todos/todobyuser/2")
    assert response.status_code == 404
    assert response.json()["detail"] == "No todo found for this user!"

def test_get_todo_by_todoid_userid():
    response = client.get("/todos/1/todobyuser/1")
    assert response.status_code == 200
    assert response.json()["title"] == "test_todo"
    assert response.json()["description"] == "test description"
    assert response.json()["status"] == "Pending"
    assert response.json()["priority"] == "Medium"
    assert response.json()["user_id"] == 1

def test_get_todo_by_todoid_userid_user_not_found():
    response = client.get("/todos/1432131/todobyuser/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_get_todo_by_todoid_userid_todo_not_found():
    response = client.get("/todos/1/todobyuser/214214312")
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"

def test_get_todo_by_priority():
    response = client.get("/todos/getbypriority/", params={"priority": "Medium"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_todo_by_priority_not_found():
    response = client.get("/todos/getbypriority/", params={"priority": "High"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Todos with this priority was not found"