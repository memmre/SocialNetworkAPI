from pydantic import BaseModel

class SignUpRequest(BaseModel):
    firstName: str
    lastName: str
    emailAddress: str
    username: str
    password: str
