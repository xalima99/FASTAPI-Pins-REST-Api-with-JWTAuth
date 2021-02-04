"""Users routes handler"""
from fastapi import APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette.status import HTTP_401_UNAUTHORIZED

from app.server.models.user import (
    UserLoginSchema, UserSchema, UserUpdatePassword
)
from app.server.models.responses import (
    response_model, error_reponse_model
)
from app.server.database.userdb import (
    add_user_to_db, retrieve_user_by_id, retrieve_user_by_email, retrieve_all_users, check_user
)
from app.server.auth.auth_handler import signJWT

router = APIRouter()

@router.post("/signup", response_description="User successfully added")
async def add_user(user: UserSchema = Body(...)):
    """signup route, allows user to create a new account, mail has to be unique,
    returns jwt token if success."""
    user = jsonable_encoder(user)
    new_user = await add_user_to_db(user)
    if new_user is None:
        raise HTTPException(detail="User Already Exists", status_code=HTTP_401_UNAUTHORIZED)
    return signJWT(new_user["_id"])

@router.post("/login")
async def user_login(user: UserLoginSchema = Body(...)):
    """Login signup, allows user to access account, returns jwt token if success."""
    user = jsonable_encoder(user)
    dbuser = await retrieve_user_by_email(user["email"].strip().lower())
    check = await check_user(user)
    if check:
        return signJWT(dbuser)
    
    raise HTTPException(detail="Wrong login details!", status_code=HTTP_401_UNAUTHORIZED)

#TESTING PURPOSE
# @router.get('/')
# async def get_users():
#     users = await retrieve_all_users()
#     if users:
#         return response_model(users, "Users data retrieved")
#     return response_model(users, "Empty List")