from typing import Optional
from ..Data.supabase import get_stock_sb, create_stock_sb, update_stock_sb, get_all_stock_sb, get_stock_type_sb, get_stock_types_sb, get_stock_export_sb, get_stock_categories_sb, get_stock_structure_sb, create_stock_category_sb, update_stock_category_sb, delete_stock_category_sb, create_stock_type_sb, update_stock_type_sb, delete_stock_type_sb, delete_stock_sb, move_stock_to_type_sb, move_type_to_category_sb
from ..models.general_model import contact_us
from fastapi import APIRouter
from ..models.stock_model import stock, StockCategoryCreate, StockCategoryUpdate, StockTypeCreate, StockTypeUpdate, MoveStockRequest, MoveTypeRequest
from fastapi import Query
from ..services.excel_export import export_stock_to_excel
from fastapi.responses import StreamingResponse


router = APIRouter()

#stock types

@router.get('/get_stock_types')
async def get_stock_types():
    try:
        response = get_stock_types_sb()
        return response
    except Exception as error:
        return {"error": error }  

@router.get('/get_stock_type/{stock_type_id}')
async def get_stock_type(stock_type_id:int):
    try:
        response = get_stock_type_sb(stock_type_id)
        return response
    except Exception as error:
        return {"error": error } 
    
#stock structure

@router.get('/get_stock_structure')
async def get_stock_structure():
    try:
        response = get_stock_structure_sb()
        return response
    except Exception as error:
        return {"error": error } 


# Stock Categories
@router.post('/create_stock_category')
async def create_stock_category(category: StockCategoryCreate):
    try:
        response = create_stock_category_sb(category.category_name)
        return response
    except Exception as error:
        return {"error": str(error)}

@router.put('/update_stock_category/{category_id}')
async def update_stock_category(category_id: int, category: StockCategoryUpdate):
    try:
        response = update_stock_category_sb(category_id, category.category_name)
        return response
    except Exception as error:
        return {"error": str(error)}

@router.delete('/delete_stock_category/{category_id}')
async def delete_stock_category(category_id: int):
    try:
        # Check if category has types before deleting
        types = get_stock_types_sb()
        category_types = [t for t in types if t.get('stock_category_id') == category_id]
        
        if category_types:
            return {"error": "Cannot delete category with existing types. Move or delete types first."}
            
        response = delete_stock_category_sb(category_id)
        return response
    except Exception as error:
        return {"error": str(error)}

# Stock Types
@router.post('/create_stock_type')
async def create_stock_type(stock_type: StockTypeCreate):
    try:
        response = create_stock_type_sb(stock_type.type_name, stock_type.stock_category_id)
        return response
    except Exception as error:
        return {"error": str(error)}

@router.put('/update_stock_type/{type_id}')
async def update_stock_type(type_id: int, stock_type: StockTypeUpdate):
    try:
        response = update_stock_type_sb(type_id, stock_type.type_name, stock_type.stock_category_id)
        return response
    except Exception as error:
        return {"error": str(error)}

@router.delete('/delete_stock_type/{type_id}')
async def delete_stock_type(type_id: int):
    try:
        # Check if type has stock items before deleting
        all_stock = get_all_stock_sb()
        type_stock = [s for s in all_stock if s.get('stock_type_id') == type_id]
        
        if type_stock:
            return {"error": "Cannot delete type with existing stock items. Move or delete items first."}
            
        response = delete_stock_type_sb(type_id)
        return response
    except Exception as error:
        return {"error": str(error)}

# Stock Items
@router.delete('/delete_stock/{stock_id}')
async def delete_stock(stock_id: int):
    try:
        response = delete_stock_sb(stock_id)
        return response
    except Exception as error:
        return {"error": str(error)}

# Move operations
@router.post('/move_stock/{stock_id}')
async def move_stock(stock_id: int, request: MoveStockRequest):
    try:
        response = move_stock_to_type_sb(stock_id, request.new_type_id)
        return response
    except Exception as error:
        return {"error": str(error)}

@router.post('/move_type/{type_id}')
async def move_type(type_id: int, request: MoveTypeRequest):
    try:
        response = move_type_to_category_sb(type_id, request.new_category_id)
        return response
    except Exception as error:
        return {"error": str(error)}

#stock 

@router.get('/get_all_stock')
async def get_all_stock():
    try:
        response = get_all_stock_sb()
        return response
    except Exception as error:
        return {"error": error }
    
@router.get('/get_stock/{stock_id}')
async def get_stock(stock_id:int):
    try:
        response = get_stock_sb(stock_id)
        return response
    except Exception as error:
        return {"error": error }    
    
@router.get('/get_stock_categories')
async def get_stock_categories():
    try:
        response = get_stock_categories_sb()
        return response
    except Exception as error:
        return {"error": error } 

@router.post('/create_stock')
async def create_stock(stock:stock):
    try:
        response = create_stock_sb(stock)
        return response
    except Exception as error:
        return {"error": error } 
    
@router.put('/update_stock/{stock_id}')
async def update_stock(stock_id:int,stock:stock):
    try:
        response = update_stock_sb(stock_id,stock)
        return response
    except Exception as error:
        return {"error": error }
    
#
@router.get('/export_stock_excel')
async def export_stock_excel():
    try:
        stock_data = get_stock_export_sb()
        
        if isinstance(stock_data, Exception):
            return {"error": str(stock_data)}
        if not stock_data:
            return {"error": "No stock data found"}
        
        excel_file = export_stock_to_excel(stock_data)
        
        return StreamingResponse(
            content=excel_file,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": "attachment; filename=stock_report.xlsx",
                "Access-Control-Expose-Headers": "Content-Disposition"
            }
        )
    except Exception as error:
        return {"error": str(error)}