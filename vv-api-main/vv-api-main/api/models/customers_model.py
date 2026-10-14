from typing import Optional
from pydantic import BaseModel
from datetime import time

class customer(BaseModel):
    title_id:Optional[int | None] = None
    name:Optional[str | None] = None
    surname:Optional[str | None] = None
    email_address:Optional[str | None] = None
    phone_number:Optional[str | None] = None
    company_name:Optional[str | None] = None
    telephone:Optional[str | None] = None
    registration_number:Optional[str | None] = None
    vat_number:Optional[str | None] = None
    address:Optional[str | None] = None

class updateCustomer(BaseModel):
    user_id:int
    company_name:str
    telephone:str
    registration_number:str
    vat_number:str
    address:str