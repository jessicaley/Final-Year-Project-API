from pydantic import BaseModel
from typing import Optional

class delivery_note(BaseModel):
    delivery_note_id: int
    job_card_id: int
    delivery_note_url: str
    created_at: Optional[str] = None
