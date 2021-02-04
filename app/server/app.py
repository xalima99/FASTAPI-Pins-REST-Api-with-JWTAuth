"""Pin Api Root Path"""
from fastapi import FastAPI
from fastapi_versioning import VersionedFastAPI

from app.server.routes.v1.pin import router as PinRouter_v1
from app.server.routes.v1.user import router as UserRouter_v1

app = FastAPI()


@app.get("/", tags=["Root"])
async def read_root():
    """Root path, Pin Api available at  http://localhost:8000/v1/docs#/"""
    return {"message": "Welcome to this fantastic app!"}

appv1 = FastAPI()
appv1.include_router(PinRouter_v1, tags=["Pins"], prefix="/pins")
appv1.include_router(UserRouter_v1, tags=["Users"], prefix="/users")

app.mount("/v1", appv1)