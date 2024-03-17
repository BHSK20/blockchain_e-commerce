from pydantic import BaseModel

class Transfer(BaseModel):
    amount: float
    currency: str
    email: str
