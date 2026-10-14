from pydantic import BaseModel
from typing import Optional

class pattern(BaseModel):
    pattern_id: int
    pattern_type_id: int
    design: str
    
