from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import get_db
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter(prefix="/tasks", tags=["Tasks API"])

class Task(BaseModel):
    title : str
    description : str | None = None
    completed : bool = False


# --- 1. CREATE TASK (POST) ---
@router.post("/")
async def create_task(task: Task, db: Session = Depends(get_db), token : str = Depends(oauth2_scheme)):
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
@router.get("/")
async def get_all_tasks(db: Session = Depends(get_db), token : str = Depends(oauth2_scheme)):
    # Yeh choti si line DB se saara data nikal layegi (SELECT * FROM tasks)
    print("User ka token hai:", token) 
    return {"tasks": db.query(models.DBTask).all()}
    
# --- 3. GET SINGLE TASK ---
@router.get("/{task_id}")
async def get_single_task(task_id: int, db: Session = Depends(get_db),token : str = Depends(oauth2_scheme)):
    # DB mein check karo jahan id = task_id ho
    db_task = db.query(models.DBTask).filter(models.DBTask.id == task_id).first()
    
    if not db_task:
        raise HTTPException(status_code=404, detail="Bhai, yeh task nahi mila!")
    return db_task

# --- 4. DELETE TASK ---
@router.delete("/{task_id}")
async def delete_task(task_id: int, db: Session = Depends(get_db),token : str = Depends(oauth2_scheme)):
    db_task = db.query(models.DBTask).filter(models.DBTask.id == task_id).first()
    
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(db_task)  # DB se uda do
    db.commit()         # Save changes
    return {"message": "Task hamesha ke liye delete ho gaya!", "deleted_task": db_task}
    
@router.put('/{task_id}')
async def update_tasks(task_id: int, update: Task,db : Session = Depends(get_db),token : str = Depends(oauth2_scheme)):
    db_task = db.query(models.DBTask).filter(models.DBTask.id == task_id).first()
    
    if not db_task:
        raise HTTPException(status_code=404,detail = "Task not found")
    
    db_task.title = update.title
    db_task.description = update.description
    db_task.completed = update.completed
    
    db.commit()
    db.refresh(db_task)
    
    return {
        'message' : "Task is updated successfully",
        'Task' : db_task
    }