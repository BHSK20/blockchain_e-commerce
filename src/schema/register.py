from pydantic import BaseModel

class Register(BaseModel):
    email: str
