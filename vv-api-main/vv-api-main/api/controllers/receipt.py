from ..Data.supabase import get_receipts_sb,get_receipt_sb,create_receipt_sb,update_receipt_sb
from fastapi import APIRouter
from ..models.receipt_model import receipt

router = APIRouter()


@router.get('/get_receipts')
async def get_receipts():
    try:
        response = get_receipts_sb()
        return response
    except Exception as error:
        return {"error": error }  

@router.get('/get_receipt/{receipt_id}')
async def get_receipt(receipt_id:int):
    try:
        response = get_receipt_sb(receipt_id)
        return response
    except Exception as error:
        return {"error": error } 
    
@router.post('/create_receipt')
async def create_receipt(receipt:receipt):
    try:
        response = create_receipt_sb(receipt)
        return response
    except Exception as error:
        return {"error": error } 
    
@router.put('/update_receipt/{receipt_id}')
async def update_receipt(receipt_id:int,receipt:receipt):
    try:
        response = update_receipt_sb(receipt_id,receipt)
        return response
    except Exception as error:
        return {"error": error } 