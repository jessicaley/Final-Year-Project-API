from ..Data.supabase import get_customers_sb,get_customer_sb,create_customer_sb,update_customer_sb,get_customer_types_sb
from fastapi import APIRouter
from ..models.customers_model import customer, updateCustomer

router = APIRouter()


@router.get('/get_customers')
async def get_customers():
    try:
        response = get_customers_sb()
        return response
    except Exception as error:
        return {"error": error }  

@router.get('/get_customer/{customer_id}')
async def get_customer(customer_id:int):
    try:
        response = get_customer_sb(customer_id)
        return response
    except Exception as error:
        return {"error": error } 
    
@router.post('/create_customer')
async def create_customer(customer:customer):
    try:
        response = create_customer_sb(customer)
        return response
    except Exception as error:
        return {"error": error } 
    
@router.put('/update_customer/{customer_id}')
async def update_customer(customer_id:int,customer:updateCustomer):
    try:
        response = update_customer_sb(customer_id,customer)
        return response
    except Exception as error:
        return {"error": error }
    
    
# Customer Types

@router.get('/get_customer_types')
async def get_customer_types():
    try:
        response = get_customer_types_sb()
        return response
    except Exception as error:
        return {"error": error }  

