"""Pins database and handlers"""
from bson import ObjectId

from app.server.database.dbconfig import pins_collection

def pin_helper(pin) -> dict:
    return {
        "id": str(pin["_id"]),
        "user_id": pin["user_id"],
        "title": pin["title"],
        "link": pin["link"],
        "comment": pin["comment"]
    }

async def retrieve_user_pins(user_id: str):
    """Retrieve all students present in the database"""
    pins = []
    async for pin in pins_collection.find({"user_id": user_id}):
        pins.append(pin_helper(pin))
    
    return pins

async def retrieve_user_pin(user_id: str, id: str) -> dict:
    """Retrieve a specific pin"""
    pin = await pins_collection.find_one({"_id": ObjectId(id), "user_id": user_id})
    if pin:
        return pin_helper(pin)

async def add_new_pin(pin_data: dict) -> dict:
    """adds a new pin in the database"""
    pin = await pins_collection.insert_one(pin_data)
    new_pin = await pins_collection.find_one({"_id": pin.inserted_id})
    return pin_helper(new_pin)

async def update_pin(user_id: str, id: str, data: dict):
    """Updates a pin"""
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    pin = await pins_collection.find_one({"_id": ObjectId(id), "user_id": user_id})
    if pin:
        updated_pin = await pins_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": {"comment": data["comment"]}}
        )
        if updated_pin:
            new_pin = await pins_collection.find_one({"_id": ObjectId(id)})
            return pin_helper(new_pin)
        return False

async def delete_pin(user_id: str, id: str):
    """Deletes a pin"""
    pin = await pins_collection.find_one({"_id": ObjectId(id), "user_id": user_id})
    if pin:
        await pins_collection.delete_one({"_id": ObjectId(id)})
        return True