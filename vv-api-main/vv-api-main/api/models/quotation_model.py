from typing import Optional
from pydantic import BaseModel
from datetime import time

class quotation(BaseModel):
    quotation_id: Optional[int| None] = None
    job_request_id: Optional[int | None] = None
    # deposit: Optional[float]
    total_cost: Optional[float]
    quotation_url: Optional[str]
    quotation_number: Optional[str]
    quotation_status_id: Optional[int | None] = None
    created_at: Optional[time] = None
