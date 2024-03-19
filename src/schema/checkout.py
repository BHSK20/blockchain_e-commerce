from pydantic import BaseModel

class Checkout(BaseModel):
    amount: float
    currency: str

class GetOrder(BaseModel):
    amount: float
    currency: str
    order_id: str