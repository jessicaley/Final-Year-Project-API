from pydantic import BaseModel
from datetime import datetime, time
from typing import Optional



class EmployeeTimeLog(BaseModel):
    employee_time_log_id: int
    clock_in: time
    clock_out: time
    employee_id: int 

class ClockCodeResponse(BaseModel):
    code: int
    expires_at: datetime
    
# New models for simplified system
class GenerateClockCodeRequest(BaseModel):
    type: str 
    
class VerifyClockCodeRequest(BaseModel):
    employee_id: int
    code: int
    type: str 
    
class GenerateClockCodeRequest(BaseModel):
    type: str
    expires_in: Optional[int] = 5