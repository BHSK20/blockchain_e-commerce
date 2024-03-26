from pydantic import BaseModel
from typing import Optional
class Transfer(BaseModel):
    amount: float
    currency: str
    email: str
    order_data: Optional[dict] = None

class TransferOrder(BaseModel):
    order_id: int