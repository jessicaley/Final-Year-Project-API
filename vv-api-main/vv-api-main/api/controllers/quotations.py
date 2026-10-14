from ..Data.supabase import get_quotations_sb,get_quotation_sb,create_quotation_sb,update_quotation_sb, get_quotation_statuses_sb, get_quotation_status_sb,get_quotations_user_sb,accept_quotation_sb,reject_quotation_sb, get_pending_quotes_sb
from fastapi import APIRouter
from ..models.quotation_model import quotation

router = APIRouter()

#quotation status

@router.get('/get_quotation_statuses')
async def get_quotation_statuses():
    try:
        response = get_quotation_statuses_sb()
        return response
    except Exception as error:
        return {"error": error }  

@router.get('/get_quotation_status/{quotation_status_id}')
async def get_quotation_status(quotation_status_id:int):
    try:
        response = get_quotation_status_sb(quotation_status_id)
        return response
    except Exception as error:
        return {"error": error }
    
#quotations    
@router.get('/get_quotations')
async def get_quotations():
    try:
        response = get_quotations_sb()
        return response
    except Exception as error:
        return {"error": error }  

@router.get('/get_quotations_user/{user_id}')
async def get_quotations_user(user_id:int):
    try:
        response = get_quotations_user_sb(user_id)
        return response
    except Exception as error:
        return {"error": error }  

@router.get('/get_quotation/{quotation_id}')
async def get_quotation(quotation_id:int):
    try:
        response = get_quotation_sb(quotation_id)
        return response
    except Exception as error:
        return {"error": error } 
    
@router.post('/create_quotation')
async def create_quotation(quotation:quotation):
    try:
        
        response = create_quotation_sb(quotation)
        return response
    except Exception as error:
        return {"error": error } 
    
@router.put('/update_quotation/{quotation_id}')
async def update_quotation(quotation_id:int,quotation:quotation):
    try:
        response = update_quotation_sb(quotation_id,quotation)
        return response
    except Exception as error:
        return {"error": error } 
    
@router.get('/accept_quotation/{quotation_id}')
async def accept_quotation(quotation_id:int):
    try:
        response = accept_quotation_sb(quotation_id)
        return response
    except Exception as error:
        return {"error": error }    
    
@router.get('/reject_quotation/{quotation_id}')
async def reject_quotation(quotation_id:int):
    try:
        response = reject_quotation_sb(quotation_id)
        return response
    except Exception as error:
        return {"error": error }       
    
@router.get('/pending_quotes')
async def get_pending_quotes():
    try:
        result = get_pending_quotes_sb()
        
        # Handle database errors
        if isinstance(result, dict) and 'error' in result:
            return {"error": result['error']}
            
        # Return sorted data by invoice number
        return sorted(result, key=lambda x: x['quotation_number'] or '')
        
    except Exception as error:
        return {"error": str(error)}