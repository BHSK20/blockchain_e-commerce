from pydantic import BaseModel

class MerchantRegister(BaseModel):
    merchant_name: str
    tax_number: str
    address: str