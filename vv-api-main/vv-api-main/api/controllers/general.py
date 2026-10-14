from ..Data.supabase import get_titles_sb,contact_us_sb,get_admin_stats_sb,get_artisan_stats_sb, get_faqs_sb, get_job_completion_timeline_sb, get_pending_job_requests_sb, get_revenue_data_sb, get_logout_timer_sb, update_logout_timer_sb
from ..models.general_model import contact_us, logout_timer
from fastapi import APIRouter

router = APIRouter()

@router.get('/get_titles')
async def get_titles():
    try:
        response = get_titles_sb()
        return response
    except Exception as error:
        return {"error": error }
       
@router.post('/contact_us')
async def contact_us(contact:contact_us):
    try:
        response = contact_us_sb(contact)
        return response
    except Exception as error:
        return {"error": error }
    
@router.get('/get_admin_stats')
async def get_admin_stats():
    try:
        response = get_admin_stats_sb()
        return response
    except Exception as error:
        return {"error": error }   
    
@router.get('/get_artisan_stats/{user_id}')
async def get_artisan_stats(user_id: int):
    try:
        response = get_artisan_stats_sb(user_id)
        return response
    except Exception as error:
        return {"error": error }   
    
@router.get('/get_faqs')
async def get_faqs():
    try:
        response = get_faqs_sb()
        return response
    except Exception as error:
        return {"error": error }
        
@router.get('/get_logout_timer/{timer_id}')
async def get_logout_timer(timer_id:int):
    try:
        response = get_logout_timer_sb(timer_id)
        return response
    except Exception as error:
        return {"error": error } 
    
@router.get('/get_job_completion_timeline')
async def get_job_completion_timeline():
    try:
        response = get_job_completion_timeline_sb()
        # Check if we got an error response
        if hasattr(response, 'code') and response.code == '42P01':
            # Table doesn't exist, return empty data
            return []
        elif isinstance(response, Exception):
            # Other error, return empty array
            return []
        else:
            return response
    except Exception as error:
        return {"error": str(error)}
 
@router.put('/update_logout_timer/{timer_id}')
async def update_logout_timer(timer_id:int,logout_timer:logout_timer):
    try:
        response = update_logout_timer_sb(timer_id,logout_timer)
        return response
    except Exception as error:
        return {"error": error } 
    
@router.get('/get_pending_job_requests')
async def get_pending_job_requests(filter: str = 'all'):
    try:
        response = get_pending_job_requests_sb(filter)
        return response
    except Exception as error:
        return {"error": str(error)}
    
@router.get('/get_revenue_data')
async def get_revenue_data():
    try:
        response = get_revenue_data_sb()
        return response
    except Exception as error:
        return {"error": str(error)}