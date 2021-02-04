"""User Model"""
from typing import Optional, List, Dict

from pydantic import BaseModel, EmailStr, Field

class UserSchema(BaseModel):
    username: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    
class UserUpdatePassword(BaseModel):
    hashed_password: Optional[str]
    
class UserLoginSchema(BaseModel):
    password: str = Field(...)
    email: EmailStr = Field(...)