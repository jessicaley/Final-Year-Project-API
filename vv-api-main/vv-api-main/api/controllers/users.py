from ..Data.supabase import get_users_sb,get_user_sb,create_user_sb,update_user_sb,get_user_employee_sb,get_user_customer_sb
from fastapi import APIRouter
from ..models.user_model import user, UserUpdate

router = APIRouter()

@router.get('/get_users')
async def get_users():
    try:
        response = get_users_sb()
        return response
    except Exception as error:
        return {"error": error }  

@router.get('/get_user/{user_id}')
async def get_user(user_id:int):
    try:
        response = get_user_sb(user_id)
        return response
    except Exception as error:
        return {"error": error } 
    
@router.get('/get_user_employee/{user_id}')
async def get_user(user_id:int):
    try:
        response = get_user_employee_sb(user_id)
        return response
    except Exception as error:
        return {"error": error }    
    
@router.get('/get_user_customer/{user_id}')
async def get_user(user_id:int):
    try:
        response = get_user_customer_sb(user_id)
        return response
    except Exception as error:
        return {"error": error }
    
    
@router.post('/create_user')
async def create_user(user:user):
    try:
        response = create_user_sb(user)
        return response
    except Exception as error:
        return {"error": error } 
    
@router.put('/update_user/{user_id}')
async def update_user(user_id: int, user: UserUpdate):  
    try:
        response = update_user_sb(user_id, user)
        return response
    except Exception as error:
        return {"error": error }