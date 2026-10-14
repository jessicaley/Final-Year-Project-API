from pydantic import BaseModel
from typing import Optional


class role(BaseModel):
    role_name: str
    description: Optional[str] = None

class role_claim(BaseModel):
    permission:str

class role_claim_line(BaseModel):
    role_claim_id:int
    role_id:int
    view:bool
    create:bool
    update:bool
    delete:bool