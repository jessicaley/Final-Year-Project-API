from pydantic import BaseModel
from datetime import time


class contact_us(BaseModel):
    subject: str
    message: int
    user_id: int

class faq(BaseModel):
    faq_id: int
    faq_q: str
    faq_a: str

class logout_timer(BaseModel):
    time: int