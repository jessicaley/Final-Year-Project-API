from pydantic import BaseModel

class receipt(BaseModel):
    receipt_id: int
    quotation_id: int
    amount_paid: float     
    