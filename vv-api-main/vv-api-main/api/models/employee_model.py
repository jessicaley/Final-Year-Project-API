from pydantic import BaseModel
from typing import Optional


class employee(BaseModel):
    job_scope:str
    address:str
    user_id:int
    emergency_contact:str
    hourly_rate:float
    
class EmployeeUpdate(BaseModel):
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
