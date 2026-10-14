from pydantic import BaseModel

class material(BaseModel):
    material_id: int
    material_name: str