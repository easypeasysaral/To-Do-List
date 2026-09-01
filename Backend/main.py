from fastapi import FastAPI,HTTPException,Depends
from pydantic import BaseModel
from typing import Optional
import models
from database import engine
from sqlalchemy.orm import Session                   # Type hinting ke liye
from database import get_db, engine                  # Humara get_db function

# Yeh jaadu wali line Postgres mein actual tables create kar degi!
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title= "This is the to-do-list API")



class Task(BaseModel):
    title : str
    description : str | None = None
    completed : bool = False

@app.get('/')
async def read_root():
    return {
        'message' : 'Backend running'
    }
# --- 1. CREATE TASK (POST) ---
@app.post("/tasks/")
async def create_task(task: Task, db: Session = Depends(get_db)):
    # Yahan hum Pydantic (Web) data ko SQLAlchemy (DB) data mein convert kar rahe hain
    new_task = models.DBTask(
        title=task.title, 
        description=task.description, 
        completed=task.completed
    )
    
    db.add(new_task)      # Data DB session mein daala
    db.commit()           # Data ko final Save kiya!
    db.refresh(new_task)  # Data ko wapas mangwaya taaki 'id' (1, 2, 3) mil sake
    
    return {"message": "Task Asli DB mein add ho gaya!", "task": new_task}

# --- 2. GET ALL TASKS (GET) ---
@app.get("/tasks/")
async def get_all_tasks(db: Session = Depends(get_db)):
    # Yeh choti si line DB se saara data nikal layegi (SELECT * FROM tasks)
    tasks = db.query(models.DBTask).all()
    return {"tasks": tasks}
    
# --- 3. GET SINGLE TASK ---
@app.get("/tasks/{task_id}")
async def get_single_task(task_id: int, db: Session = Depends(get_db)):
    # DB mein check karo jahan id = task_id ho
    db_task = db.query(models.DBTask).filter(models.DBTask.id == task_id).first()
    
    if not db_task:
        raise HTTPException(status_code=404, detail="Bhai, yeh task nahi mila!")
    return db_task

# --- 4. DELETE TASK ---
@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(models.DBTask).filter(models.DBTask.id == task_id).first()
    
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(db_task)  # DB se uda do
    db.commit()         # Save changes
    return {"message": "Task hamesha ke liye delete ho gaya!", "deleted_task": db_task}
    
@app.put('/tasks/{task_id}')
async def update_tasks(task_id: int, update: Task,db : Session = Depends(get_db)):
    db_task = db.query(models.DBTask).filter(models.DBTask.id == task_id).first()
    
    if not db_task:
        raise HTTPException(status_code=404,details = "Task not found")
    
    db_task.title = update.title
    db_task.description = update.description
    db_task.completed = update.completed
    
    db.commit()
    db.refresh(db_task)
    
    return {
        'message' : "Task is updated successfully",
        'Task' : db_task
    }
    
