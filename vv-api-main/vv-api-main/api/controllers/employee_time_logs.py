from datetime import datetime, timedelta
import random
from fastapi import APIRouter, Query, HTTPException, status
from ..Data.supabase import (get_employee_time_logs_sb, get_employee_time_log_sb, get_monthly_hours_worked, verify_clock_code_sb, clock_in_sb, clock_out_sb, invalidate_previous_codes, create_clock_code_sb, get_employee_by_phone_sb, get_employee_time_logs_by_id_sb)
from ..models.employee_time_log_model import VerifyClockCodeRequest, GenerateClockCodeRequest, ClockCodeResponse

router = APIRouter()

@router.get('/get_employee_time_logs')
async def get_employee_time_logs():
    try:
        response = get_employee_time_logs_sb()
        return response
    except Exception as error:
        return {"error": error }  

@router.get('/get_employee_time_log/{employee_time_log_id}')
async def get_employee_time_log(employee_time_log_id:int):
    try:
        response = get_employee_time_log_sb(employee_time_log_id)
        return response
    except Exception as error:
        return {"error": error } 
    
@router.get('/monthly_hours_worked')
async def monthly_hours_worked_report(year: int = Query(..., description="Year to generate report for")):

    try:
        result = get_monthly_hours_worked(year)
        
        if isinstance(result, dict) and 'error' in result:
            return {"error": result['error']}
            
        #  sorted data by month number 
        return sorted(result, key=lambda x: x['month_number'])
        
    except Exception as error:
        return {"error": error }
    
@router.post('/generate-clock-code')
async def generate_clock_code(request: GenerateClockCodeRequest):
    try:
        # Generate
        code = random.randint(100000, 999999)
        expires_at = datetime.utcnow() + timedelta(minutes=request.expires_in)
        
        response = create_clock_code_sb(code, request.type, expires_at)
        
        return {"code": code, "expires_at": expires_at.isoformat(), "expires_in": request.expires_in}
    
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating code: {str(error)}"
        )

@router.post('/verify-clock-code')
async def verify_clock_code(request: VerifyClockCodeRequest):
    try:
        verification = verify_clock_code_sb(request.code, request.type)
        
        if not verification['valid']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=verification['message']
            )
        
        #  time of entry
        current_time = datetime.utcnow().isoformat()
        if request.type == 'clock_in':
            response = clock_in_sb(request.employee_id, current_time)
        else:
            response = clock_out_sb(request.employee_id, current_time)
        
        return {"status": "success", "message": f"Clocked {request.type} successfully"}
    
    except HTTPException as he:
        raise he
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Verification failed: {str(error)}"
        )

@router.post('/clock-in')
async def clock_in(employee_id: int):
    try:
        # Get time
        clock_in_time = datetime.now().isoformat()
        
        response = clock_in_sb(employee_id, clock_in_time)
        return {"status": "success", "clock_in_time": clock_in_time}
    
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Clock in failed: {str(error)}"
        )

@router.post('/clock-out')
async def clock_out(employee_id: int):
    try:
        # Get  time
        clock_out_time = datetime.now().isoformat()
        
        response = clock_out_sb(employee_id, clock_out_time)
        return {"status": "success", "clock_out_time": clock_out_time}
    
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Clock out failed: {str(error)}"
        )
        
@router.get('/employees/get-by-phone/{phone}')
async def get_employee_by_phone(phone: str):
    try:
        #  formatting 
        clean_phone = ''.join(filter(str.isdigit, phone))
        
        employee = get_employee_by_phone_sb(clean_phone)
        
        if not employee:
            raise HTTPException(
                status_code=404,
                detail="Employee not found for this phone number"
            )
        
        return {
            "employee_id": employee['employee_id'],
            "user_id": employee['user_id']
        }
        
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(error)}"
        )
        
@router.get('/get_employee_time_logs_by_id/{employee_id}')
async def get_employee_time_logs_by_id(employee_id: int):
    try:
        response = get_employee_time_logs_by_id_sb(employee_id)
        return response
    except Exception as error:
        return {"error": str(error)}