from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title= "This is the to-do-list API")

fake_db = []

class Task(BaseModel):
    title : str
    description : str | None = None
    completed : bool = False

@app.get('/')
async def read_root():
    return {
        'message' : 'Backend running'
    }

@app.get('/allTasks')
def get_allTasks():
    return{
        'tasks' : fake_db
    }

@app.get('/tasks/{task_id}')
async def get_task(task_id:int,q:str|None = None):
    if q:
        return {
            "task_id" : task_id,
            "query" : q
        }
    return {
        "task_id" : task_id,
        "message" : "No query"
    }

@app.post("/tasks/")
async def create_task(task:Task):
    fake_db.append(task)
    return {
        'message' : "new task created successfully",
        "data_recieved" : task
    }