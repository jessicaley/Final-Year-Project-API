from pydantic import BaseModel


class employee_pay_slip(BaseModel):
    employee_id:int
    salary:float
    payslip_url:str