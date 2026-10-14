# job_card_model.py
from pydantic import BaseModel
from typing import Optional, List

class job_card(BaseModel):
    job_card_id: int  
    pattern_id: Optional[int] = None
    job_card_status_id: Optional[int] = None
    quotation_id: Optional[int] = None
    special_instructions: Optional[str] = None
    completed_at: Optional[str] = None

    
class JobCardUpdate(BaseModel):
    pattern_id: Optional[int] = None
    job_card_status_id: Optional[int] = None
    quotation_id: Optional[int] = None
    special_instructions: Optional[str] = None
    completed_at: Optional[str] = None
    materials: Optional[List[int]] = None
    artisans: Optional[List[int]] = None
    

class JobCardBase(BaseModel):
    pattern_id: Optional[int] = None
    job_card_status_id: Optional[int] = None
    quotation_id: Optional[int] = None
    special_instructions: Optional[str] = None
    completed_at: Optional[str] = None

class JobCardCreate(JobCardBase):
    materials: List[int] = []
    artisans: List[int] = []

class JobCard(JobCardBase):
    job_card_id: int

class Material(BaseModel):
    material_id: int
    material_name: str

class JobCardWithMaterials(JobCard):
    materials: List[Material] = []