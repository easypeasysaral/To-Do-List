from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import Optional
import models
from database import engine

# Yeh jaadu wali line Postgres mein actual tables create kar degi!
models.Base.metadata.create_all(bind=engine)

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
    
@app.get('/tasks/{task_id}')
async def get_single_task(task_id : int ):
    if task_id<0 or task_id>=len(fake_db):
        raise HTTPException(status_code=404, detail=f"task with {task_id} not found")
    return fake_db[task_id]

@app.delete('/tasks/{task_id}')
async def delete_task(task_id : int):
    if task_id<0 or task_id>=len(fake_db):
        raise HTTPException(status_code=404, detail=f"task with {task_id} not found")
    
    deleted_task = fake_db.pop(task_id)
    return {
        'message' : "Task deleted successfully",
        'Deleted_task'  : deleted_task
    }
    
@app.put('/tasks/{task_id}')
async def update_tasks(task_id: int, update: Task):
    if task_id<0 or task_id>=len(fake_db):
        raise HTTPException(status_code=404, detail = f"The task with the {task_id} not found")
    
    fake_db[task_id] = update
    
    return {
        'message' : "Task updated successfully",
        'task' : update
    }
