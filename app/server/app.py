"""Pin Api Root Path"""
from fastapi import FastAPI, Request, Response
from fastapi_versioning import VersionedFastAPI
#Imports for rate limiter
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.server.routes.v1.pin import router as PinRouter_v1
from app.server.routes.v1.user import router as UserRouter_v1

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/", tags=["Root"])
# @limiter.limit("5/minute")
async def read_root(request: Request, response: Response):
    """Root path, Pin Api available at  http://localhost:8000/v1/docs#/"""
    return {"message": "Welcome to this fantastic app!"}

appv1 = FastAPI()
appv1.include_router(PinRouter_v1, tags=["Pins"], prefix="/pins")
appv1.include_router(UserRouter_v1, tags=["Users"], prefix="/users")

app.mount("/v1", appv1)