from pydantic import BaseModel

class GetPayload(BaseModel):
    token: str

class GetMerchantInfo(BaseModel):
    email: str