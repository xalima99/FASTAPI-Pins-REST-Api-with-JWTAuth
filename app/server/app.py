from fastapi import FastAPI

from app.server.routes.pin import router as PinRouter
from app.server.routes.user import router as UserRouter

app = FastAPI()
app.include_router(PinRouter, tags=["Pins"], prefix="/pins")
app.include_router(UserRouter, tags=["Users"], prefix="/users")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}