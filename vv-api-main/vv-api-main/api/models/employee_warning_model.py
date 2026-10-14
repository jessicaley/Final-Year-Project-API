from pydantic import BaseModel


class employee_warning(BaseModel):
    reason:str
    employee_warning_type_id:int
    employee_id:int
    is_disputed:bool