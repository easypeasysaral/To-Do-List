from fastapi import FastAPI,HTTPException,Depends,APIRouter
from pydantic import BaseModel
from typing import Optional
import models
from database import engine
from sqlalchemy.orm import Session                   # Type hinting ke liye
from database import get_db, engine                  # Humara get_db function
from routers import tasks
from fastapi.security import OAuth2PasswordRequestForm
# Yeh jaadu wali line Postgres mein actual tables create kar degi!
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title= "This is the to-do-list API")

@app.get('/')
async def read_root():
    return {
        'message' : 'Backend running'
    }


app.include_router(tasks.router)

@app.post("/login")
async def login(formData:OAuth2PasswordRequestForm = Depends()):
    if(formData.username == 'admin' and formData.password == 'secret'):
        return {
            'access_token' : "Saral",
            'token_type' : 'bearer'
        }
        
        return HTTPException(status_code=400,detail="Invalid username or password")
