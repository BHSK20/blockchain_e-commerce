from pydantic import BaseModel
from typing import Optional
class MerchantRegister(BaseModel):
    merchant_name: str
    country: str
    zipcode: int
    city: str
    address1: str
    address2: Optional[str] = None