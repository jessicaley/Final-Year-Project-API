from ..Data.supabase import get_roles_sb,get_role_sb,create_role_sb,update_role_sb,get_role_claims_sb,get_role_claim_lines_sb,create_role_claim_line_sb,update_role_claim_line_sb, delete_role_sb
from fastapi import APIRouter
from ..models.role_model import role, role_claim, role_claim_line

router = APIRouter()


@router.get('/get_roles')
async def get_roles():
    try:
        response = get_roles_sb()
        return response
    except Exception as error:
        return {"error": error }  

@router.get('/get_role/{role_id}')
async def get_role(role_id:int):
    try:
        response = get_role_sb(role_id)
        return response
    except Exception as error:
        return {"error": error } 
    
@router.post('/create_role')
async def create_role(role:role):
    try:
        response = create_role_sb(role)
        return response
    except Exception as error:
        return {"error": error } 
    
@router.put('/update_role/{role_id}')
async def update_role(role_id:int,role:role):
    try:
        response = update_role_sb(role_id,role)
        return response
    except Exception as error:
        return {"error": error } 
    


@router.get('/get_role_claims')
async def get_role_claims():
    try:
        response = get_role_claims_sb()
        return response
    except Exception as error:
        return {"error": error }  
    


@router.get('/get_role_claim_lines')
async def get_role_claim_lines():
    try:
        response = get_role_claim_lines_sb()
        return response
    except Exception as error:
        return {"error": error }  
    
@router.post('/create_role_claim_line')
async def create_role_claim_line(role_claim_line:role_claim_line):
    try:
        response = create_role_claim_line_sb(role_claim_line)
        return response
    except Exception as error:
        return {"error": error } 
    
@router.put('/update_role_claim_line/{role_claim_id}/{role_id}')
async def update_role_claim_line(role_claim_id:int,role_id:int,role_claim_line:role_claim_line):
    try:
        response = update_role_claim_line_sb(role_claim_id,role_id,role_claim_line)
        return response
    except Exception as error:
        return {"error": error } 
    
@router.delete('/delete_role/{role_id}')
async def delete_role(role_id:int):
    try:
        response = delete_role_sb(role_id)
        return response
    except Exception as error:
        return {"error": error}