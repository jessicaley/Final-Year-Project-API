from ..Data.supabase import get_pattern_sb, get_patterns_sb, create_pattern_sb, get_pattern_type_sb, get_pattern_types_sb, delete_pattern_sb
from fastapi import APIRouter
from ..models.pattern_model import pattern

router = APIRouter()


@router.get('/get_patterns')
async def get_patterns():
    try:
        response = get_patterns_sb()
        return response
    except Exception as error:
        return {"error": error }
    
@router.get('/get_pattern/{pattern_id}')
async def get_pattern(pattern_id:int):
    try:
        response = get_pattern_sb(pattern_id)
        return response
    except Exception as error:
        return {"error": error }    

@router.post('/create_pattern')
async def create_pattern(pattern: pattern):
    try:
        response = create_pattern_sb(pattern)
        return response
    except Exception as error:
        return {"error": str(error)}
    
@router.get('/get_pattern_types')
async def get_pattern_type():
    try:
        response = get_pattern_types_sb()
        return response
    except Exception as error:
        return {"error": error }
    
@router.get('/get_pattern_type/{pattern_type_id}')
async def get_pattern_type(pattern_type_id:int):
    try:
        response = get_pattern_type_sb(pattern_type_id)
        return response
    except Exception as error:
        return {"error": error }  
    
@router.delete('/delete_pattern/{pattern_id}')
async def delete_pattern(pattern_id: int):
    try:
        response = delete_pattern_sb(pattern_id)
        return response
    except Exception as error:
        return {"error": error}