from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    full_name: str
    username: str
    email: EmailStr
    password: str
    role: str

class UserLogin(BaseModel):
    username: str
    password: str

    