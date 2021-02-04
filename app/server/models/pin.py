"""Pin Model"""
from pydantic import BaseModel, Field
from typing import Optional

class PinDbSchema(BaseModel):
    comment: str = Field(...)
    title: str = Field(...)
    link: str = Field(...)
    user_id: str = Field(...)
 
   
class PinSchema(BaseModel):
    comment: str = Field(...)
    link: str = Field(...)


class UpdatePinModel(BaseModel):
    comment: Optional[str]
    
