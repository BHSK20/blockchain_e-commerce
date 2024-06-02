from pydantic import BaseModel
from datetime import date

class GetPayload(BaseModel):
    token: str

class GetMerchantInfo(BaseModel):
    email: str
    
class UpdateUserInfo(BaseModel):
    name: str
    card_number: int
    date_of_birth: date
    nationality: str
    gender: str # True if female