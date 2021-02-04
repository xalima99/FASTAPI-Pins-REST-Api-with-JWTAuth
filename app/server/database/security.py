"""Password Hasher and decrypter helpers"""
import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED


pwd_context = CryptContext(schemes=["bcrypt"])


def get_hashed_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False
    
