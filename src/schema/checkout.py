from pydantic import BaseModel

class Checkout(BaseModel):
    amount: int
    currency: str
    order_id: str
