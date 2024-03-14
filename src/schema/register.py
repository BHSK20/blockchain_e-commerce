from pydantic import BaseModel

class Register(BaseModel):
    name: str
    email: str
    password: str

class VerifyAccount(BaseModel):
    token: str
