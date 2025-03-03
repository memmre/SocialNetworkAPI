from pydantic import BaseModel

class SignInRequest(BaseModel):
    identifier: str
    password: str
