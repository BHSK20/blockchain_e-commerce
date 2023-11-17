from pydantic import BaseModel

class Register(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

class VerifyAccount(BaseModel):
    token: str
