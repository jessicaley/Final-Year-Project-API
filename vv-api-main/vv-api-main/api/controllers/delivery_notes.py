from ..Data.supabase import get_delivery_note_sb, create_delivery_note_sb, get_delivery_notes_sb, delete_delivery_note_sb, get_delivery_notes_user_sb
from fastapi import APIRouter
from ..models.delivery_note_model import delivery_note

router = APIRouter()

    
@router.get('/get_delivery_notes')
async def get_delivery_notes():
    try:
        response = get_delivery_notes_sb()
        return response
    except Exception as error:
        return {"error": error }  

@router.get('/get_delivery_note/{delivery_note}')
async def get_delivery_note(delivery_note_id:int):
    try:
        response = get_delivery_note_sb(delivery_note_id)
        return response
    except Exception as error:
        return {"error": error } 
    
@router.post('/create_delivery_note')
async def create_delivery_note(delivery_note:delivery_note):
    try:
        response = create_delivery_note_sb(delivery_note)
        return response
    except Exception as error:
        return {"error": error } 
    
@router.delete('/delete_delivery_note/{delivery_note_id}')
async def delete_delivery_note(delivery_note_id: int):
    try:
        response = delete_delivery_note_sb(delivery_note_id)
        return response
    except Exception as error:
        return {"error": error}
    
@router.get('/get_devlivery_notes_user/{user_id}')
async def get_devlivery_notes_user(user_id:int):
    try:
        response = get_delivery_notes_user_sb(user_id)
        return response
    except Exception as error:
        return {"error": error } 
     
