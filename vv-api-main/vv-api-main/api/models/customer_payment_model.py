from pydantic import BaseModel
from datetime import time

class customer_payment(BaseModel):
    customer_payment_id:int
    quotation_id:int
    customer_payment_status_id:int
    amount_paid:float