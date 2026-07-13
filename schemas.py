from typing import Optional

from pydantic import BaseModel, EmailStr


# -----------------------------
# USER SCHEMAS
# -----------------------------

class UserCreate(BaseModel):
    full_name: str
    username: str
    email: EmailStr
    password: str
    role: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    user_id: str
    full_name: str
    username: str
    email: EmailStr
    role: str
    is_active: int


# -----------------------------
# CONTACT SCHEMAS
# -----------------------------

class ContactCreate(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    phone: str
    email: EmailStr
    company: str
    job_title: Optional[str] = None
    city: str


class ContactUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    company: Optional[str] = None
    job_title: Optional[str] = None
    city: Optional[str] = None


class ContactResponse(BaseModel):
    contact_id: str
    first_name: str
    last_name: Optional[str] = None
    phone: str
    email: EmailStr
    company: str
    job_title: Optional[str] = None
    city: str
    created_at: str


class ChangePassword(BaseModel):

    current_password: str

    new_password: str