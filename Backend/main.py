from fastapi import FastAPI,HTTPException,Depends,APIRouter
from pydantic import BaseModel
from typing import Optional
import models
from database import engine
from sqlalchemy.orm import Session                   # Type hinting ke liye
from database import get_db, engine                  # Humara get_db function
from routers import tasks
from fastapi.security import OAuth2PasswordRequestForm
import jwt
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

# Yeh jaadu wali line Postgres mein actual tables create kar degi!
models.Base.metadata.create_all(bind=engine)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
# Isey int() se integer mein convert karna bohot zaroori hai!
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

def create_access_token(data: dict):
    to_encode = data.copy()
    
    # Expiry time set karna (Abhi ke time se 30 minute aage)
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # Token ko JWT library se encrypt (encode) karke taala lagana
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

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
        token = create_access_token(data={'sub':formData.username})
        return {
            'access_token' : token,
            'token_type' : 'bearer'
        }
        
    raise HTTPException(status_code=400,detail="Invalid username or password")

