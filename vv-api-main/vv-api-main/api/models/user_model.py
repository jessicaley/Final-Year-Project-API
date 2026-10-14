from pydantic import BaseModel
from typing import Optional

class user(BaseModel):
    name:str
    surname:str
    email_address:str
    phone_number:str
    role_id:int
    title_id:int
    image:str
    uuid:str
    is_employee:bool

class UserUpdate(BaseModel):
    email_address: Optional[str] = None
    phone_number: Optional[str] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    image: Optional[str] = None
