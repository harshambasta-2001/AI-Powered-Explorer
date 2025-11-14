from pydantic import BaseModel,EmailStr,model_validator
from datetime import datetime
from typing import Optional
from app.utils.enum import *
import json

class TokenData(BaseModel): 
    id: Optional[str] = None

class UserCreate(BaseModel):
    email: EmailStr
    username:str
    role: Optional[UserRole] = UserRole.USER
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TaskCreate(BaseModel):
    prompt_or_query: Optional[str] = None

class TaskUpdate(BaseModel):
    notes: Optional[str] = None
    content: Optional[str] = None
    prompt_or_query: Optional[str] = None




