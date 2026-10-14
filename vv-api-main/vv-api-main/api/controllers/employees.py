from ..Data.supabase import get_types_sb,get_type_sb,create_type_sb,update_type_sb,get_employees_sb,get_employee_sb, \
    create_employee_sb,update_employee_sb,get_pay_slips_sb,get_pay_slip_sb,create_pay_slip_sb,update_pay_slip_sb \
    ,get_employee_warnings_sb,get_employee_warning_sb,create_employee_warning_sb,update_employee_warning_sb,delete_employee_warning_sb,get_time_logs_sb,clock_in_sb,clock_out_sb, get_artisans_sb
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from ..Data.supabase import (
    get_types_sb, get_type_sb, create_type_sb, update_type_sb,
    get_employees_sb, get_employee_sb, create_employee_sb, update_employee_sb,
    get_pay_slips_sb, get_pay_slip_sb, create_pay_slip_sb, update_pay_slip_sb,
    get_employee_warnings_sb, get_employee_warning_sb, create_employee_warning_sb, update_employee_warning_sb,
    get_time_logs_sb, clock_in_sb, clock_out_sb, get_artisans_sb,
    get_employee_info_sb, get_user_by_phone_sb, get_employee_by_user_id_sb, get_user_sb
)
from ..models.type_model import type
from ..models.employee_model import employee
from ..models.employee_pay_slip_model import employee_pay_slip
from ..models.employee_warning_model import employee_warning

router = APIRouter()

# Pydantic model for employee update
class EmployeeUpdate(BaseModel):
    emergency_contact: Optional[str] = None
    address: Optional[str] = None


# -------------------------------
# Employee Types
# -------------------------------
@router.get('/get_types')
async def get_types():
    try:
        return get_types_sb()
    except Exception as error:
        return {"error": error}

@router.get('/get_type/{type_id}')
async def get_type(type_id: int):
    try:
        return get_type_sb(type_id)
    except Exception as error:
        return {"error": error}

@router.post('/create_type')
async def create_type(type: type):
    try:
        return create_type_sb(type)
    except Exception as error:
        return {"error": error}

@router.put('/update_type/{type_id}')
async def update_type(type_id: int, type: type):
    try:
        return update_type_sb(type_id, type)
    except Exception as error:
        return {"error": error}


# -------------------------------
# Employees
# -------------------------------
@router.get('/get_employees')
async def get_employees():
    try:
        return get_employees_sb()
    except Exception as error:
        return {"error": error}

@router.get('/get_employee/{employee_id}')
async def get_employee(employee_id: int):
    try:
        return get_employee_sb(employee_id)
    except Exception as error:
        return {"error": error}

@router.post('/create_employee')
async def create_employee(employee: employee):
    try:
        return create_employee_sb(employee)
    except Exception as error:
        return {"error": error}

@router.get('/employee/info/{employee_id}')
async def get_employee_info(employee_id: int):
    try:
        employee_data = get_employee_info_sb(employee_id)
        if isinstance(employee_data, Exception) or "error" in employee_data:
            raise HTTPException(status_code=500, detail=str(employee_data))
        return employee_data
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

@router.get('/employee/user/{user_id}')
async def get_employee_by_user_id(user_id: int):
    try:
        employee_data = get_employee_by_user_id_sb(user_id)
        if isinstance(employee_data, Exception) or "error" in employee_data:
            raise HTTPException(status_code=500, detail=str(employee_data))
        return employee_data
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

@router.get('/get_user_by_phone/{phone}')
async def get_user_by_phone(phone: str):
    try:
        user_data = get_user_by_phone_sb(phone)
        if isinstance(user_data, Exception) or "error" in user_data:
            raise HTTPException(status_code=500, detail=str(user_data))
        return user_data
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

@router.put('/employee/update/{employee_id}')
async def update_employee(employee_id: int, employee: EmployeeUpdate):
    try:
        employee_data = employee.dict(exclude_unset=True)
        response = update_employee_sb(employee_id, employee_data)
        if isinstance(response, Exception) or "error" in response:
            raise HTTPException(status_code=500, detail=str(response))
        return {"success": True, "data": response}
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

@router.get('/employee/profile/{employee_id}')
async def get_employee_profile(employee_id: int):
    try:
        employee_data = get_employee_info_sb(employee_id)
        if isinstance(employee_data, Exception) or "error" in employee_data or len(employee_data) == 0:
            raise HTTPException(status_code=404, detail="Employee not found")

        employee = employee_data[0]
        user_id = employee.get("user_id")
        if not user_id:
            return employee_data

        user_data = get_user_sb(user_id)
        if isinstance(user_data, Exception) or "error" in user_data or len(user_data) == 0:
            return employee_data

        user = user_data[0]
        merged_data = {**employee, **user}
        return [merged_data]
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


# -------------------------------
# Employee Pay Slips
# -------------------------------
@router.get('/get_pay_slips')
async def get_pay_slips():
    try:
        return get_pay_slips_sb()
    except Exception as error:
        return {"error": error}

@router.get('/get_pay_slip/{pay_slip_id}')
async def get_pay_slip(pay_slip_id: int):
    try:
        return get_pay_slip_sb(pay_slip_id)
    except Exception as error:
        return {"error": error}

@router.post('/create_pay_slip')
async def create_pay_slip(pay_slip: employee_pay_slip):
    try:
        return create_pay_slip_sb(pay_slip)
    except Exception as error:
        return {"error": error}

@router.put('/update_pay_slip/{pay_slip_id}')
async def update_pay_slip(pay_slip_id: int, pay_slip: employee_pay_slip):
    try:
        return update_pay_slip_sb(pay_slip_id, pay_slip)
    except Exception as error:
        return {"error": error}


# -------------------------------
# Employee Warnings
# -------------------------------
@router.get('/get_employee_warnings')
async def get_employee_warnings():
    try:
        return get_employee_warnings_sb()
    except Exception as error:
        return {"error": error}

@router.get('/get_employee_warning/{employee_warning_id}')
async def get_employee_warning(employee_warning_id: int):
    try:
        return get_employee_warning_sb(employee_warning_id)
    except Exception as error:
        return {"error": error}

@router.post('/create_employee_warning')
async def create_employee_warning(employee_warning: employee_warning):
    try:
        return create_employee_warning_sb(employee_warning)
    except Exception as error:
        return {"error": error}

@router.put('/update_employee_warning/{employee_warning_id}')
async def update_employee_warning(employee_warning_id: int, employee_warning: employee_warning):
    try:
        return update_employee_warning_sb(employee_warning_id, employee_warning)
    except Exception as error:
        return {"error": error } 
    
@router.delete('/delete_employee_warning/{employee_warning_id}')
async def delete_employee_warning(employee_warning_id:int):
    try:
        response = delete_employee_warning_sb(employee_warning_id)
        return response
    except Exception as error:
        return {"error": error } 


# -------------------------------
# Time Logs & Artisans
# -------------------------------
@router.get('/get_time_logs')
async def get_time_logs():
    try:
        return get_time_logs_sb()
    except Exception as error:
        return {"error": error}

@router.post('/clock_in/{employee_id}')
async def clock_in(employee_id: int):
    try:
        return clock_in_sb(employee_id)
    except Exception as error:
        return {"error": error}

@router.post('/clock_out/{employee_id}')
async def clock_out(employee_id: int):
    try:
        return clock_out_sb(employee_id)
    except Exception as error:
        return {"error": error}

@router.get('/get_artisans')
async def get_artisans():
    result = get_artisans_sb()
    if isinstance(result, Exception):
        raise HTTPException(status_code=500, detail=f"Error fetching artisans: {str(result)}")
    return result
