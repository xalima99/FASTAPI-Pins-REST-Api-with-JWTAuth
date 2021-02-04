"""Databases config using AsyncIoMotor with MongoDb"""
import motor.motor_asyncio
from bson.objectid import ObjectId

MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

pins = client.pins
users = client.users

pins_collection = pins.get_collection("pins_collection")
users_collection = users.get_collection("users_collection")