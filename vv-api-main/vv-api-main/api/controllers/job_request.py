from ..Data.supabase import get_job_requests_sb,get_job_request_sb,create_job_request_sb,update_job_request_sb,reject_job_request_sb,get_job_requests_user_sb, cancel_job_request_sb
from fastapi import APIRouter
from ..models.job_request_model import job_request, job_request_insert
from fastapi import  HTTPException


router = APIRouter()


@router.get('/get_job_requests')
async def get_job_requests():
    try:
        response = get_job_requests_sb()
        return response
    except Exception as error:
        return {"error": error }  

@router.get('/get_job_requests_user/{user_id}')
async def get_job_requests(user_id:int):
    try:
        response = get_job_requests_user_sb(user_id)
        return response
    except Exception as error:
        return {"error": error } 

@router.get('/get_job_request/{job_request_id}')
async def get_job_request(job_request_id:int):
    try:
        response = get_job_request_sb(job_request_id)
        return response
    except Exception as error:
        return {"error": error } 
    
@router.post('/create_job_request')
async def create_job_request(job_request:job_request_insert):
    try:
        response = create_job_request_sb(job_request)
        return response
    except Exception as error:
        return {"error": error } 
    
@router.put('/update_job_request/{job_request_id}')
async def update_job_request(job_request_id:int,job_request:job_request):
    try:
        response = update_job_request_sb(job_request_id,job_request)
        return response
    except Exception as error:
        return {"error": error }
    
@router.get('/reject_job_request/{job_request_id}')
async def reject_job_request(job_request_id:int):
    try:
        response = await reject_job_request_sb(job_request_id)
        return response
    except Exception as error:
        return {"error": error }   
    

@router.put('/cancel_job_request/{job_request_id}')
async def cancel_job_request(job_request_id: int):
    try:
        # Call the synchronous function
        result = cancel_job_request_sb(job_request_id)
        
        # Check if we got an error response
        if isinstance(result, dict) and "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        # Return success response
        return {"success": True, "message": "Job request cancelled", "data": result}
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
