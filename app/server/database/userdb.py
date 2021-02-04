"""User database and handlers"""
from app.server.database.dbconfig import users_collection
from app.server.database.security import get_hashed_password, verify_password
from bson import ObjectId
from app.server.models.user import UserLoginSchema
from app.server.auth.auth_handler import signJWT, decodeJWT

def user_helper(user):
    return {
        "_id": str(user["_id"]),
        "email": user["email"].strip().lower()
    }

async def check_user(user):
    try:
        dbuser = await users_collection.find_one({"email": user["email"].lower().strip()})
        if dbuser and verify_password(user["password"], dbuser["hashed_password"]):
            return True
    except Exception as e:
        print(e)
        return False
    
    return False

async def retrieve_all_users():
    """Retrieve all users present in the database"""
    try:
        users = []
        async for user in users_collection.find():
            users.append(user_helper(user))
        return users
    except Exception as e:
        print(e)
        pass


async def retrieve_user_by_id(id: str):
    """Retrieve single user if present in the database"""
    try:
        user = await users_collection.find({"_id": ObjectId(id)})
        if user:
            return user_helper(user)
    except Exception as e:
        print(e)
        pass
    
async def retrieve_user_by_email(email: str):
    """Retrieve single user if present in the database"""
    try:
        user = await users_collection.find_one({"email": email})
        if user:
            return user_helper(user)
    except Exception as e:
        print(e)
        return None
    
    return None
    
async def add_user_to_db(user: dict):
    """adds user in the database"""
    try:
        dbuser = await users_collection.find_one({"email": user["email"].strip().lower()})
        if dbuser:
            return None
        user["email"] = user["email"].strip().lower()
        user["hashed_password"] = get_hashed_password(user["password"])
        user.pop("password")
        
        dbuse = await users_collection.insert_one(user)
        new_user = await users_collection.find_one({"_id": dbuse.inserted_id})
        return user_helper(new_user)
    except Exception as e:
        print(e)
        return None
