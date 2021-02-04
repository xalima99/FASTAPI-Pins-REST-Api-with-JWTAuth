"""Pins routes handler"""
from bson import ObjectId
from fastapi import APIRouter, Body, Depends, HTTPException, Path
from fastapi.encoders import jsonable_encoder
from starlette.status import (HTTP_400_BAD_REQUEST, 
                              HTTP_503_SERVICE_UNAVAILABLE, 
                              HTTP_404_NOT_FOUND,
                              HTTP_401_UNAUTHORIZED)

from app.server.auth.auth_bearer import JWTBearer
from app.server.auth.auth_handler import decodeJWT
from app.server.helpers.titler import get_title

from app.server.database.pindb import (
    add_new_pin,
    retrieve_user_pin,
    retrieve_user_pins,
    update_pin,
    delete_pin
)

from app.server.models.pin import (
    PinSchema,
    UpdatePinModel
)

from app.server.models.responses import (
    error_reponse_model,
    response_model
)

router = APIRouter()

@router.get("/", response_description="All user's Pins")
async def get_user_pins(token: str = Depends(JWTBearer())):
    """Gets all pins from DB"""
    infos = decodeJWT(token)
    try:
        all_pins = await retrieve_user_pins(infos["user_id"]["_id"])
        return response_model(all_pins, "Pins fetched successfully")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=HTTP_503_SERVICE_UNAVAILABLE, 
                            detail="Something went wrong, please retry")


@router.get("/{pin_id}", response_description="User's Pin")
async def get_user_single_pin(pin_id: str = Path(..., title="The ID of the Pin to get"), 
                              token: str = Depends(JWTBearer())):
    """Gets specific pin from DB"""
    infos = decodeJWT(token)
    try:
        pin = await retrieve_user_pin(infos["user_id"]["_id"], pin_id)
        if pin:
            return response_model(pin, "Pin fetched successfully")
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Pin not found in DB")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Bad Request") 


@router.put("/{pin_id}", response_description="User's Pin Updated")
async def update_user_pin(data: UpdatePinModel = Body(...), 
                          pin_id: str = Path(..., title="The ID of the Pin to update"), 
                          token: str = Depends(JWTBearer())):
    """Updates specific pin from DB"""
    infos = decodeJWT(token)
    try:
        jsondata = jsonable_encoder(data)
        pin = await update_pin(infos["user_id"]["_id"], pin_id, jsondata)
        if pin:
            return response_model(pin, "Pin successfully Updated")
        else:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="You are not authorized")
    except Exception as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Bad Request")
    
    raise HTTPException(status_code=HTTP_503_SERVICE_UNAVAILABLE, detail="Something went wrong")


@router.delete("/{pin_id}", response_description="Pin successfully deleted")
async def delete_user_pin(pin_id: str = Path(..., title="The ID of the Pin to delete"), 
                          token: str = Depends(JWTBearer())):
    """Deletes specific pin from DB"""
    infos = decodeJWT(token)
    userId = infos["user_id"]["_id"]

    try:
        pin = await delete_pin(userId, pin_id)
        if pin:
            return response_model(pin, "Pin Deleted successfully")
        else:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="You are not authorized")
    except Exception as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Bad Request")
    
    raise HTTPException(status_code=HTTP_503_SERVICE_UNAVAILABLE, detail="Something went wrong")


@router.post("/", response_description="Pin successfully added")
async def add_pin(pin: PinSchema = Body(...), token: str = Depends(JWTBearer())):
    """creates a new pin"""
    infos = decodeJWT(token)
    pin = jsonable_encoder(pin)
    
    #check if the link is valid and if yes extract title
    check = get_title(pin["link"])
    
    if check["status"] == 400:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Provided Link is not valid")
    
    pin["title"] = check["title"]
    pin["user_id"] = infos["user_id"]["_id"]
    try:
        new_pin = await add_new_pin(pin)
        return response_model(new_pin, "Pin added successfully.")
    except expression as identifier:
        raise HTTPException(status_code=HTTP_503_SERVICE_UNAVAILABLE, 
                            detail="Something went wrong, please retry")
    
    
    