from pydantic import BaseModel
from typing import Optional

class stock(BaseModel):
    stock_id: int
    stock_type_id: int
    material_id: int
    name: str
    description: str
    stock_level: int
    stock_price: float
    
# Define request models
class StockCategoryCreate(BaseModel):
    category_name: str

class StockCategoryUpdate(BaseModel):
    category_name: str

class StockTypeCreate(BaseModel):
    type_name: str
    stock_category_id: int

class StockTypeUpdate(BaseModel):
    type_name: str
    stock_category_id: int

class MoveStockRequest(BaseModel):
    new_type_id: int

class MoveTypeRequest(BaseModel):
    new_category_id: int