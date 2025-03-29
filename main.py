from fastapi import FastAPI

app = FastAPI()


todos = [
    {"todo_id" : 1, "title": "Make dinner", "completed" : False},
    {"todo_id": 2, "title": "Work out", "completed" : True},
    {"todo_id": 3, "title": "Clean up", "completed" : False},
    {"todo_id": 4, "title": "Learn python", "completed" : True},
]
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI, I'm Luka!"}

@app.get("/todos/{todo_id}")
def get_todo(todo_id):
    for todo in todos:
        if todo["todo_id"] == todo_id:
            return {"result": todo}

#http://127.0.0.1:8000/todos
@app.get("/todos")
def get_todos():
    return todos