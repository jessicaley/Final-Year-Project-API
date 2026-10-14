from pydantic import BaseModel
from typing import Optional

class invoice(BaseModel):
    invoice_number: str
    total: float
    invoice_url: str
    invoice_status_id: int = 2
    pop: Optional[str] = None
    quote_id: Optional[int] = None  