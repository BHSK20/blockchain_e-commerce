from pydantic import BaseModel

class Header(BaseModel):
    merchant: int
    sign: str
    api_key: str

class HeaderUserPayload(BaseModel):
    authorization: str